import os
from PIL import Image
import cStringIO

from django.db.models.fields.files import ImageFieldFile
from django.db.models import FileField, ImageField
from django.core.files.base import ContentFile
from django.db.models.fields import NOT_PROVIDED

from south.modelsinspector import add_introspection_rules

from .... import forms

class DefaultImageFieldFile(ImageFieldFile):
    def __init__(self, *args, **kwargs):
        super(DefaultImageFieldFile, self).__init__(*args, **kwargs)
        self.default_url = self.field.default_url
        
    def _get_url(self):
        try:
            return super(DefaultImageFieldFile, self)._get_url()
        except ValueError:
            return self.default_url
    url = property(_get_url)

class ImageWithThumbsFieldFile(DefaultImageFieldFile):
    """
    See ImageWithThumbsField for usage example
    """
    def __init__(self, *args, **kwargs):
        super(ImageWithThumbsFieldFile, self).__init__(*args, **kwargs)
        
        if self.field.sizes:
            for size in self.field.sizes:
                setattr(self, 'url_%sx%s' % (size[0],size[1]), self._get_thumb_url(size))

    def _get_thumb_path(self, size):
        head, tail = os.path.split(self.name)
        thumb_dir = '%sx%s' % (size[0], size[1])
        return os.path.join(head, thumb_dir, tail)

    def _get_thumb_url(self, size):
        head, tail = self.url.rsplit('/',1)
        thumb_dir = '%sx%s' % (size[0], size[1])
        return "/".join((head,thumb_dir,tail))

    def _generate_thumb(self, img, thumb_size, format):
        """
        Generates a thumbnail image and returns a ContentFile object with the thumbnail
        
        Parameters:
        ===========
        img         File object
        
        thumb_size  desired thumbnail size, ie: (200,120)
        
        format      format of the original image ('jpeg','gif','png',...)
                    (this format will be used for the generated thumbnail, too)
        """
        img.seek(0) # see http://code.djangoproject.com/ticket/8222 for details
        image = Image.open(img)

        # Convert to RGB if necessary
        if image.mode not in ('L', 'RGB', 'RGBA'):
            image = image.convert('RGB')

        # get size
        thumb_w, thumb_h = thumb_size
        # If you want to generate a square thumbnail
        if thumb_w == thumb_h:
            # quad
            xsize, ysize = image.size
            # get minimum size
            minsize = min(xsize,ysize)
            # largest square possible in the image
            xnewsize = (xsize-minsize)/2
            ynewsize = (ysize-minsize)/2
            # crop it
            image2 = image.crop((xnewsize, ynewsize, xsize-xnewsize, ysize-ynewsize))
            # load is necessary after crop                
            image2.load()
            # thumbnail of the cropped image (with ANTIALIAS to make it look better)
            image2.thumbnail(thumb_size, Image.ANTIALIAS)
        else:
            # not quad
            image2 = image
            image2.thumbnail(thumb_size, Image.ANTIALIAS)

        io = cStringIO.StringIO()
        # PNG and GIF are the same, JPG is JPEG
        if format.upper()=='JPG':
            format = 'JPEG'
        image2.save(io, format)
        return ContentFile(io.getvalue())

    def save(self, name, content, save=True):
        super(ImageWithThumbsFieldFile, self).save(name, content, save)
        
        if self.field.sizes:
            for size in self.field.sizes:
                thumb_path = self._get_thumb_path(size)
                split = self.name.rsplit('.',1)
                
                # you can use another thumbnailing function if you like
                thumb_content = self._generate_thumb(content, size, split[1])
                thumb_path_ = self.storage.save(thumb_path, thumb_content)
                
                if not thumb_path == thumb_path_:
                    raise ValueError('There is already a file %s' % thumb_path)
        
    def delete(self, save=True):
        name=self.name
        super(ImageWithThumbsFieldFile, self).delete(save)
        if self.field.sizes:
            for size in self.field.sizes:
                thumb_path = self._get_thumb_path(size)
                try:
                    self.storage.delete(thumb_path)
                except:
                    pass

class RemovableFileField(FileField):
    def _delete_file(self, instance):
        if getattr(instance, self.attname):
            file_name = getattr(instance, self.name).path
            # If the file exists and no other object of this type references it,
            # delete it from the filesystem.
            if os.path.exists(file_name) and \
                not instance.__class__._default_manager.filter(**{'%s__exact' % self.name: getattr(instance, self.attname)}).exclude(pk=instance._get_pk_val()):
                os.remove(file_name)

    def get_internal_type(self):
        return 'FileField'

    def save_form_data(self, instance, data):
        if data:
            if not data[1]:
                # replace file
                self._delete_file(instance)
                super(RemovableFileField, self).save_form_data(instance, data[0])
            else:
                # delete file
                self._delete_file(instance)
                setattr(instance, self.name, None)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.RemovableFileField}
        defaults.update(kwargs)
        return super(RemovableFileField, self).formfield(**defaults)

class RemovableImageField(ImageField, RemovableFileField):
    attr_class = DefaultImageFieldFile

    def __init__(self, *args, **kwargs):
        self.default_url = kwargs.pop('default', None)
        if self.default_url:
            kwargs['blank'] = True
        super(RemovableImageField, self).__init__(self, *args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.RemovableImageField}
        defaults.update(kwargs)
        return super(RemovableImageField, self).formfield(**defaults)

class ImageWithThumbsField(RemovableImageField):
    attr_class = ImageWithThumbsFieldFile
    """
    Usage example:
    ==============
    photo = ImageWithThumbsField(upload_to='images', sizes=((125,125),(300,200),)
    
    To retrieve image URL, exactly the same way as with ImageField:
        my_object.photo.url
    To retrieve thumbnails URL's just add the size to it:
        my_object.photo.url_125x125
        my_object.photo.url_300x200
    
    Note: The 'sizes' attribute is not required. If you don't provide it, 
    ImageWithThumbsField will act as a normal ImageField
        
    How it works:
    =============
    For each size in the 'sizes' atribute of the field it generates a 
    thumbnail with that size and stores it following this format:
    
    available_filename.[width]x[height].extension

    Where 'available_filename' is the available filename returned by the storage
    backend for saving the original file.
    
    Following the usage example above: For storing a file called "photo.jpg" it saves:
    photo.jpg          (original file)
    photo.125x125.jpg  (first thumbnail)
    photo.300x200.jpg  (second thumbnail)
    
    With the default storage backend if photo.jpg already exists it will use these filenames:
    photo_.jpg
    photo_.125x125.jpg
    photo_.300x200.jpg
    
    Note: django-thumbs assumes that if filename "any_filename.jpg" is available 
    filenames with this format "any_filename.[widht]x[height].jpg" will be available, too.
    
    To do:
    ======
    Add method to regenerate thubmnails
    
    """
    def __init__(self, width_field=None, height_field=None, sizes=None, **kwargs):
        self.width_field=width_field
        self.height_field=height_field
        self.sizes = sizes
        super(ImageWithThumbsField, self).__init__(**kwargs)

rules = [
        (
            (ImageWithThumbsField, ),
            [],
            {
                "width_field":  ["width_field",  {"default": None}],
                "height_field": ["height_field", {"default": None}],
                "sizes":        ["sizes",        {"default": None}],
                "default":      ["default",      {"default": None}],
            },
        ),
    ]

add_introspection_rules(rules, ["^k2\.utils\.django\.db\.models\.fields\.files\.ImageWithThumbsField"])

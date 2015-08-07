"""Stories models module"""

from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
from django.contrib.comments.moderation import CommentModerator, moderator
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from tagging.fields import TagField
from tagging.models import Tag
from tagging.utils import parse_tag_input

from threadedcomments.models import ThreadedComment

from k2.utils.voting.models import Vote
from k2.utils.django.contrib.moderation import RelatedModerator

from k2.stories import settings as stories_settings
from k2.stories import managers
from k2.stories import signals
from k2.profiles.models import USERCLASS_CHOICE_ROOKIE

RATING_STYLE_SUM, RATING_STYLE_APART = False, True

RATING_STYLE_CHOICES = (
    (RATING_STYLE_SUM, _('sum')),
    (RATING_STYLE_APART, _('apart')),
)

SORT_CHOICE_POPULAR, SORT_CHOICE_NEW, SORT_CHOICE_COMMENTED = 1, 2, 3

SORT_CHOICES = (
    (SORT_CHOICE_POPULAR, _('popular')),
    (SORT_CHOICE_NEW, _('new')),
    (SORT_CHOICE_COMMENTED, _('commented')),
)

class Category(models.Model):
    """Category model class"""
    parent      = models.ForeignKey('self', related_name='children', \
                    verbose_name=_('parent'), null=True, blank=True, \
                    db_index=True)
    name        = models.CharField(_('name'), max_length=50)
    slug        = models.SlugField()
    position    = models.PositiveSmallIntegerField(_('position'), default=0)
    summary     = models.TextField(_('summary'), blank=True)
    enable_stories = models.BooleanField(_('enable stories'), default=True)

    objects = managers.CategoryManager()
    top_categories = managers.TopCategoryManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('position', 'name')

    def __unicode__(self):
        return self.name

#    def save(self, *args, **kwargs):
#        if not self.id:
#            self.slug = slugify(self.name)
#        super(Category, self).save(*args, **kwargs)

    def url(self):
        return reverse('stories:category', args=[self.slug])

    def has_parent(self):
        return self.parent != None
    has_parent.boolean = True

class Story(models.Model):
    """Story model class"""
    user          = models.ForeignKey(User, related_name='stories', \
                        verbose_name=_('author'))
    url             = models.URLField(_('url address'), unique=True)
    title           = models.CharField(_('title'), max_length=255, help_text=_("Wpisz krotki i dobrze opisujacy strone tytul (maks. 255 znakow)."))
    slug            = models.SlugField()
    summary         = models.TextField(_('summary'), help_text=_("Podaj opis strony (2 do 4 zdan)."))
    category        = models.ForeignKey(Category, related_name='stories', \
                        verbose_name=_('category'))
    created_date    = models.DateTimeField(_('created date'), \
                        auto_now_add=True, editable=False)
    published_date  = models.DateTimeField(_('published date'), blank=True, \
                        null=True, editable=False)
    enable_comments = models.BooleanField(_('enable comments'), default=True)
    registration_required = models.BooleanField(_('registration required'), help_text=_("If this is checked, only logged-in users will be able to view the page."), default=False)
    karma           = models.IntegerField(_('karma'), default=0, editable=False)
    digs_count      = models.PositiveIntegerField(_('digs count'), default=0, \
                        editable=False)
    buries_count    = models.PositiveIntegerField(_('buries count'), default=0, \
                        editable=False)
    comments_count  = models.PositiveIntegerField(_('comments count'), \
                        default=0, editable=False)
    ip_address  = models.IPAddressField(_('IP address'), blank=True, null=True)
    is_public   = models.BooleanField(_('is public'), default=True,
                    help_text=_('Uncheck this box to make the story effectively ' \
                                'disappear from the site.'))
    is_locked  = models.BooleanField(_('is locked'), default=False,
                    help_text=_('Check this box if you don\'t want publish the story. ' \
                                'Story will be available only via direct link.'))
    is_removed  = models.BooleanField(_('is removed'), default=False,
                    help_text=_('Check this box if the story is inappropriate. ' \
                                'A "This story has been removed" message will ' \
                                'be displayed instead.'))
    # userlists
    watched     = models.ManyToManyField(User, related_name='watched', \
                        verbose_name=_('Waches'), through='Watch', \
                        blank=True, null=True)
    saved          = models.ManyToManyField(User, related_name='saved', \
                        verbose_name=_('Saves'), through='Save', \
                        blank=True, null=True)
    # generics
    votes           = generic.GenericRelation(Vote)
    comments        = generic.GenericRelation(Comment, object_id_field='object_pk')
#    def set_tags(self, tags):
#        Tag.objects.update_tags(self, tags)

#    def get_tags(self):
#        return Tag.objects.get_for_object(self)

#    tags            = property(_get_tags, _set_tags)
    tags            = TagField(help_text=_("Podaj etykiety, ktore najlepiej opisuja twoje znalezisko (min. 3 znaki). Tagi oddziel przecinkami."))

    objects = managers.StoryManager()
    open = managers.OpenStoryManager()
    accessible = managers.AccessibleStoryManager()

    class Meta:
        verbose_name = _('story')
        verbose_name_plural = _('stories')
        ordering = ('published_date', )
        permissions = [("can_moderate", "Can moderate stories")]

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Story, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('stories:story_slug', args=[self.id, self.slug])

    def is_published(self):
        return self.published_date != None

    def is_editable(self):
        return datetime.now() - self.created_date < \
            timedelta(minutes=stories_settings.STORY_EDIT_TIME)

    @property
    def story_url(self):
        return self.get_absolute_url()

    @property
    def frame_url(self):
        return reverse('stories:frame_slug', args=[self.id, self.slug])

    @property
    def return_url(self):
        if self.is_published:
            # @todo: return published list
            return reverse('stories:story_slug', args=[self.id, self.slug])
        else:
            # @todo: return vaiting list
            return reverse('stories:story_slug', args=[self.id, self.slug])

    @property
    def tag_list(self):
        return parse_tag_input(self.tags)

class StoryCommentModerator(CommentModerator):
    """Comments (for story) moderation class"""
    enable_field = 'enable_comments'

    def moderate(self, comment, content_object, request):
        already_moderated = super(StoryCommentModerator,self).moderate(comment, content_object, request)
        if already_moderated:
            return True
        if request.user.profile.userclass == USERCLASS_CHOICE_ROOKIE:
            return True
        return False

class StoryModerator(RelatedModerator):
    """Story moderation class"""
    enable_field = 'enable_stories'
    related_class = Story
    related_field = 'category'
    pre_save_signal = signals.story_will_be_posted
    post_save_signal = signals.story_was_posted

    def connect(self):
        """
        Hook up the moderation methods to pre- and post-save signals
        from the objects models.

        """
        signals.story_will_be_posted.connect(self.pre_save_moderation, sender=Story)
        signals.story_was_posted.connect(self.post_save_moderation, sender=Story)

    def allow(self, story, category, request):
        """
        Determine whether a given story is allowed to be posted on
        a given category.

        Return ``True`` if the story should be allowed, ``False
        otherwise.

        """
        if self.enable_field:
            if not getattr(category, self.enable_field) and not request.user.is_superuser():
                return False
        if self.auto_close_field and self.close_after is not None:
            close_after_date = getattr(category, self.auto_close_field)
            if close_after_date is not None and self._get_delta(datetime.datetime.now(), close_after_date).days >= self.close_after:
                return False
        return True

    def moderate(self, story, content_object, request):
        already_moderated = super(StoryModerator,self).moderate(story, content_object, request)
        if already_moderated:
            return True
        if request.user.profile.userclass == USERCLASS_CHOICE_ROOKIE:
            return True
        return False

    def pre_save_moderation(self, sender, story, request, **kwargs):
        """
        Apply any necessary pre-save moderation steps to new
        story.

        """
        # Object will be disallowed outright (HTTP 403 response)
        if not self.allow(story, story.category, request): 
            return False

        if self.moderate(story, story.category, request):
            story.is_public = False

    def post_save_moderation(self, sender, story, request, **kwargs):
        """
        Apply any necessary post-save moderation steps to new
        story.

        """
        self.email(story, story.category, request)

moderator.register(Story, StoryCommentModerator)
moderator.register(Category, StoryModerator)

class StoryFlag(models.Model):
    """
    Records a flag on a story. This is intentionally flexible; right now, a
    flag could be:

        * A "removal suggestion" -- where a user suggests a story for (potential) removal.

        * A "moderator deletion" -- used when a moderator deletes a story.

    You can (ab)use this model to add other flags, if needed. However, by
    design users are only allowed to flag a story with a given flag once;
    if you want rating look elsewhere.
    """
    user      = models.ForeignKey(User, verbose_name=_('user'), related_name="story_flags")
    story     = models.ForeignKey(Story, verbose_name=_('story'), related_name="flags")
    flag      = models.CharField(_('flag'), max_length=30, db_index=True)
    flag_date = models.DateTimeField(_('date'), default=None)

    # Constants for flag types
    SUGGEST_REMOVAL = "removal suggestion"
    MODERATOR_DELETION = "moderator deletion"
    MODERATOR_APPROVAL = "moderator approval"
    MODERATOR_LOCK = "moderator lock"

    class Meta:
        db_table = 'story_flags'
        unique_together = [('user', 'story', 'flag')]
        verbose_name = _('story flag')
        verbose_name_plural = _('story flags')

    def __unicode__(self):
        return "%s flag of story ID %s by %s" % \
            (self.flag, self.story_id, self.user.username)

    def save(self, *args, **kwargs):
        if self.flag_date is None:
            self.flag_date = datetime.now()
        super(StoryFlag, self).save(*args, **kwargs)

class UserPref(models.Model):
    user = models.OneToOneField(User, related_name='pref', verbose_name=_('user'), unique=True)
    comment_threshold = models.SmallIntegerField(_('comments visibility threshold'), help_text=_('Show comments with above score.'), default=-10)
    comment_rating_style = models.BooleanField(_('comments rating style'), choices=RATING_STYLE_CHOICES, help_text=_('As default show comment score negative and positive apart. Unselected choice shown in tooltip.'), default=False)
    frame = models.BooleanField(_('use story frame'), help_text=_('Select to use frame on click story title.'), default=False)
    upcoming_sort = models.PositiveSmallIntegerField(_('upcoming sort order'), choices=SORT_CHOICES, default=SORT_CHOICE_POPULAR, editable=False)
    popular_sort = models.PositiveSmallIntegerField(_('popular sort order'), choices=SORT_CHOICES, default=SORT_CHOICE_NEW, editable=False)

    class Meta:
        verbose_name = _('preference')
        verbose_name_plural = _('preferences')

    def __unicode__(self):
        return self.user.username

    def is_rating_style_sum(self):
        return self.rating_style == RATING_STYLE_SUM

    def is_rating_style_apart(self):
        return self.rating_style == RATING_STYLE_APART

class Reference(models.Model):
    user            = models.ForeignKey(User, related_name='references', \
                        verbose_name=_('author'))
    story           = models.ForeignKey(Story, related_name='references', verbose_name=_('story'))
    url             = models.URLField(_('url address'), unique=True)
    title           = models.CharField(_('title'), max_length=255)
    created_date    = models.DateTimeField(_('created date'), \
                        auto_now_add=True, editable=False)
    votes           = generic.GenericRelation(Vote)
    ip_address  = models.IPAddressField(_('IP address'), blank=True, null=True)
    is_public   = models.BooleanField(_('is public'), default=True,
                    help_text=_('Uncheck this box to make the reference effectively ' \
                                'disappear from the site.'))
    is_removed  = models.BooleanField(_('is removed'), default=False,
                    help_text=_('Check this box if the comment is inappropriate. ' \
                                'A "This reference has been removed" message will ' \
                                'be displayed instead.'))
    class Meta:
        verbose_name = _('reference')
        verbose_name_plural = _('references')
        ordering = ('created_date', )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('stories:references_slug', args=[self.story_id, self.story.slug])

class Watch(models.Model):
    user            = models.ForeignKey(User, verbose_name=_('user'))
    story           = models.ForeignKey(Story, verbose_name=_('story'))
    last_seen       = models.DateTimeField(_('last seen'), auto_now=True, editable=False)
    date_added      = models.DateTimeField(_('date added'), auto_now_add=True, editable=False)

    class Meta:
        unique_together = (('user', 'story'),)

    def __unicode__(self):
        return str(self.user) + ': ' + str(self.story)
    
class Save(models.Model):
    user            = models.ForeignKey(User, verbose_name=_('user'))
    story           = models.ForeignKey(Story, verbose_name=_('story'))
    date_added      = models.DateTimeField(_('date added'), auto_now_add=True, editable=False)

    class Meta:
        unique_together = (('user', 'story'),)

    def __unicode__(self):
        return str(self.user) + ': ' + str(self.story)

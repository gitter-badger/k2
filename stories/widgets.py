from django import forms
from django.utils import simplejson
from django.utils.safestring import mark_safe

from tagging.models import Tag

from k2.stories.models import Story

class AutoCompleteTagInput(forms.TextInput):
    class Media:
        css = {
            'all': ('css/jquery.autocomplete.css',)
        }
        js = (
            'js/jquery.min.js',
            'js/lib/jquery.bgiframe.min.js',
            'js/lib/jquery.ajaxQueue.js',
            'js/jquery.autocomplete.min.js'
        )

    def render(self, name, value, attrs=None):
        html = super(AutoCompleteTagInput, self).render(name, value, attrs)
        page_tags = Tag.objects.usage_for_model(Story)
        tag_list = simplejson.dumps([tag.name for tag in page_tags],
                                    ensure_ascii=False)
        js = mark_safe(u'''<script type="text/javascript">
            jQuery("#id_%s").autocomplete(%s, {
                width: 150,
                max: 10,
                highlight: false,
                multiple: true,
                multipleSeparator: ", ",
                scroll: true,
                scrollHeight: 300,
                matchContains: true,
                autoFill: true,
            });
            </script>''' % (name, tag_list))
        return html + js
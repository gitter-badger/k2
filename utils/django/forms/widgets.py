from django import forms
from django.utils.html import escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

class DeleteCheckboxWidget(forms.CheckboxInput):
    def render(self, name, value, attrs=None):
        return u'<label for="%s">%s %s</label>' % (attrs['id'], super(DeleteCheckboxWidget, self).render(name, value, attrs), _('Delete'))

class RemovableFileWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (forms.FileInput(), DeleteCheckboxWidget())
        super(RemovableFileWidget, self).__init__(widgets, attrs=attrs)
    def decompress(self, value):
        # the clear checkbox is never initially checked
        self.value = value
        return [value, None]
    def format_output(self, rendered_widgets):
        if self.value:
            return rendered_widgets[0] + rendered_widgets[1]
        return rendered_widgets[0]

class CheckboxSelectMultipleGrouped(forms.CheckboxSelectMultiple):
    """
    Expects the ``choices`` list to contain 3-tuples (value, label,
    group_instance).
    """
    def render(self, name, value, attrs=None):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul>']
        str_values = set(
            [force_unicode(v) for v in value]) # Normalize to strings.
        group = None
        for i, (option_value, option_label, option_group) \
                in enumerate(self.choices):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if option_group != group:
                if group:
                    output.append('</ul></li>')
                group = option_group
                if has_id:
                    final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                cb = forms.CheckboxInput(
                    final_attrs, check_test=lambda value: value in str_values)
                rendered_cb = cb.render(name, option_group)
                output.append(u'<li><label>%s %s</label><ul>' % (
                    rendered_cb, escape(force_unicode(group))))
                #output.append(u'<li>%s<ul>' % smart_unicode(group))
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
            cb = forms.CheckboxInput(
                final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            output.append(u'<li><label>%s %s</label></li>' % (
                rendered_cb, escape(force_unicode(option_label))))
        if group:
            output.append('</ul></li>')
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))

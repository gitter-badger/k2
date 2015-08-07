from django.forms import models

from widgets import CheckboxSelectMultipleGrouped

class GroupedQuerySetIterator(models.ModelChoiceIterator):
    def __init__(self, field):
        super(GroupedQuerySetIterator, self).__init__(field)

    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label, u"")
        for obj in self.field.queryset:
            yield (obj.pk,
                   self.field.label_from_instance(obj),
                   getattr(obj, self.field.group_field_name))
        # Clear the QuerySet cache if required.
        if not self.field.cache_choices:
            self.queryset._result_cache = None

class ModelGroupedChoiceField(models.ModelChoiceField):
    """
    A MultipleChoiceField whose choices are a model QuerySet and the choices
    are grouped by a foreign key.
    """
    def __init__(self, queryset, **kwargs):
        self.group_field_name = kwargs.pop('group_field_name', None)
        kwargs.setdefault('widget', CheckboxSelectGrouped)
        super(ModelGroupedChoiceField, self).__init__(
            queryset, **kwargs)

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedQuerySetIterator(self)
    choices = property(
        _get_choices, models.ModelChoiceField._set_choices)

class ModelMultipleGroupedChoiceField(models.ModelMultipleChoiceField):
    """
    A MultipleChoiceField whose choices are a model QuerySet and the choices
    are grouped by a foreign key.
    """
    def __init__(self, queryset, **kwargs):
        self.group_field_name = kwargs.pop('group_field_name', None)
        kwargs.setdefault('widget', CheckboxSelectMultipleGrouped)
        super(ModelMultipleGroupedChoiceField, self).__init__(
            queryset, **kwargs)

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedQuerySetIterator(self)
    choices = property(
        _get_choices, models.ModelMultipleChoiceField._set_choices)

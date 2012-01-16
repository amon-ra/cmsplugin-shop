from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode, smart_str
from django.forms import Field, CheckboxInput, ChoiceField, MultipleHiddenInput, CheckboxSelectMultiple
from django.forms.util import ErrorList, ValidationError
from django.core import exceptions
from django.db import models
from django import forms


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^cmsplugin_userorders\.fields\.MultiSelectField"])
    add_introspection_rules([], ["^cmsplugin_userorders\.fields\.MultipleCheckboxField"])
    add_introspection_rules([], ["^cmsplugin_userorders\.fields\.CheckboxField"])
except:
    pass



class CheckboxField(Field):
    widget = CheckboxInput
    default_error_messages = {
        'invalid_choice': _(u'Select a valid choice. %(value)s is not one of the available choices.'),
    }

    def __init__(self, choices=(), required=True, widget=None, label=None, initial=None, help_text=None, *args, **kwargs):
        super(ChoiceField, self).__init__(required, widget, label, initial,  help_text, *args, **kwargs)
        self.choices = choices

    def _get_choices(self):
        return self._choices

    def _set_choices(self, value):
        # Setting choices also sets the choices on the widget.
        # choices can be any iterable, but we call list() on it because
        # it will be consumed more than once.
        self._choices = self.widget.choices = list(value)

    choices = property(_get_choices, _set_choices)

    def clean(self, value):
        """
        Validates that the input is in self.choices.
        """
        value = super(ChoiceField, self).clean(value)
        if value in EMPTY_VALUES:
            value = u''
        value = smart_unicode(value)
        if value == u'':
            return value
        if not self.valid_value(value):
            raise ValidationError(self.error_messages['invalid_choice'] % {'value': value})
        return value

    def valid_value(self, value):
        "Check to see if the provided value is a valid choice"
        for k, v in self.choices:
            if type(v) in (tuple, list):
                # This is an optgroup, so look inside the group for options
                for k2, v2 in v:
                    if value == smart_unicode(k2):
                        return True
            else:
                if value == smart_unicode(k):
                    return True
        return False

class MultipleCheckboxField(ChoiceField):
    hidden_widget = MultipleHiddenInput
    widget = CheckboxSelectMultiple
    default_error_messages = {
        'invalid_choice': _(u'Select a valid choice. %(value)s is not one of the available choices.'),
        'invalid_list': _(u'Enter a list of values.'),
    }

    def clean(self, value):
        """
        Validates that the input is a list or tuple.
        """
        if self.required and not value:
            raise ValidationError(self.error_messages['required'])
        elif not self.required and not value:
            return []
        if not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages['invalid_list'])
        new_value = [smart_unicode(val) for val in value]
        # Validate that each value in the value list is in self.choices.
        for val in new_value:
            if not self.valid_value(val):
                raise ValidationError(self.error_messages['invalid_choice'] % {'value': val})
        return new_value


class MultiSelectFormField(forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple

    def __init__(self, *args, **kwargs):
        self.max_choices = kwargs.pop('max_choices', 0)
        super(MultiSelectFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        if value and self.max_choices and len(value) > self.max_choices:
            raise forms.ValidationError('You must select a maximum of %s choice%s.'
                    % (apnumber(self.max_choices), pluralize(self.max_choices)))
        return value

class MultiSelectField(models.Field):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "CharField"

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def _get_FIELD_display(self, field):
        value = getattr(self, field.attname)
        choicedict = dict(field.choices)

    def formfield(self, **kwargs):
        # don't call super, as that overrides default widget if it has choices
        defaults = {'required': not self.blank, 'label': capfirst(self.verbose_name),
                    'help_text': self.help_text, 'choices':self.choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_db_prep_value(self, value):
        if isinstance(value, basestring):
            return value
        elif isinstance(value, list):
            return ",".join(value)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        elif value==None:
            return ''
        return value.split(",")

    def contribute_to_class(self, cls, name):
        super(MultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            func = lambda self, fieldname = name, choicedict = dict(self.choices):",".join([choicedict.get(value,value) for value in getattr(self,fieldname)])
            setattr(cls, 'get_%s_display' % self.name, func)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def validate(self, value, model_instance):
        arr_choices = self.get_choices_selected(self.get_choices_default())
        for opt_select in value:
            if (opt_select not in arr_choices):
                raise exceptions.ValidationError(self.error_messages['invalid_choice'] % value)
        return

    def get_choices_selected(self, arr_choices=''):
        if not arr_choices:
            return False
        list = []
        for choice_selected in arr_choices:
            list.append(choice_selected[0])
        return list

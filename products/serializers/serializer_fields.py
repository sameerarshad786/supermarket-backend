from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from psycopg2.extras import NumericRange

from rest_framework import serializers
from rest_framework.utils.formatting import lazy_format


class DecimalRangeFieldSerializer(serializers.DictField):
    default_error_messages = {
        'invalid': _('Not a valid number.'),
        'blank': _('This field may not be blank.'),
        'lower': _('lower field may not be blank.'),
        'min_value': _('Ensure this field has at least {min_value}.'),
        'max_value': _('Ensure this field has value more than {max_value}.'),
    }

    def __init__(self, **kwargs):
        self.min_value = kwargs.pop('min_value', None)
        self.max_value = kwargs.pop('max_value', None)
        super().__init__(**kwargs)

        if self.min_value:
            message = lazy_format(
                self.error_messages['min_value'], min_value=self.min_value)
            self.validators.append(
                MinValueValidator(self.min_value, message=message))

        if self.max_value:
            message = lazy_format(
                self.error_messages['max_value'], max_value=self.max_value)
            self.validators.append(
                MaxValueValidator(self.max_value, message=message))

    def to_internal_value(self, data):
        if not data:
            return self.fail('blank')
        lower = data.get("lower")
        upper = data.get("upper")
        if not lower:
            return self.fail('lower')
        return NumericRange(
            float(lower), float(upper) if upper else None, '(]')

    def to_representation(self, value):
        data = dict()
        is_elasticsearch = self.context.get("is_elasticsearch", False)

        if is_elasticsearch:
            data["lower"] = value.gt
            try:
                data["upper"] = value.lt
            except AttributeError:
                data["upper"] = None
        else:
            data["lower"] = value.lower
            try:
                data["upper"] = value.upper
            except AttributeError:
                data["upper"] = None
        return data

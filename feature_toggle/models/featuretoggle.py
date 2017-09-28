# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from djutil.models import TimeStampedModel

from feature_toggle.exceptions import FeatureToggleAttributeDoesNotExist, FeatureToggleAttributeAlreadyExists
from feature_toggle import constants
from feature_toggle.utilities import format_to_date
from feature_toggle.validators import validate_feature_toggle_code


class FeatureToggle(TimeStampedModel):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20, validators=[validate_feature_toggle_code])
    environment = models.CharField(max_length=50, choices=constants.FeatureToggle.Environment.CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{name}({code}) | {env}".format(name=self.name, code=self.code, env=self.environment)

    def __unicode__(self):
        return "{name}({code}) | {env}".format(name=self.name, code=self.code, env=self.environment)

    class Meta:
        unique_together = (('name', 'environment'), ('code', 'environment'))

    def set_attribute(self, key, value=None, update_if_existing=True):
        """
        sets up the given an attribute. If existing will update else will create.

        :param key: name of the attribute
        :param value: value of the attribute
        :param update_if_existing: If false will raise Exception
        """
        # todo: assert for key types?
        if key in (constants.FeatureToggle.Attributes.START_DATE, constants.FeatureToggle.Attributes.END_DATE):
            value = format_to_date(value) if value else value

        attrib, created = self.attributes.get_or_create(key=key)
        if not created and not update_if_existing:
            raise FeatureToggleAttributeAlreadyExists(**dict(key=key))

        attrib.value = value
        attrib.save()

    def get_attribute(self, key, raise_does_not_exist=False):
        """
        gets the value of the attribute
        :param key: name of the attribute
        :return: value or None
        """

        try:
            attr = self.attributes.get(key=key)
            return attr.value
        except ObjectDoesNotExist:
            if raise_does_not_exist:
                FeatureToggleAttributeDoesNotExist(**dict(key=key))
            return None

    @property
    def start_date(self):
        return self.get_attribute(constants.FeatureToggle.Attributes.START_DATE)

    @property
    def end_date(self):
        return self.get_attribute(constants.FeatureToggle.Attributes.END_DATE)

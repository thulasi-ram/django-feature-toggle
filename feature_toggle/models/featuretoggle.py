# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from djutil.models import TimeStampedModel

from constants import Environments
from feature_toggle.exceptions import FeatureToggleAttributeDoesNotExist, FeatureToggleAttributeAlreadyExists
from utilities import django_model_choices_from_iterable

CHOICES = django_model_choices_from_iterable(getattr(settings, 'FEATURE_TOGGLE_ENV_CHOICES', Environments))


class FeatureToggle(TimeStampedModel):
    uid = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    environment = models.CharField(max_length=50, choices=CHOICES)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    time_bomb = models.BooleanField(default=False)

    def __str__(self):
        return "{e}: {n}({u})".format(e=self.environment, n=self.name, u=self.uid)

    def __unicode__(self):
        return self.__str__()

    class Meta:
        unique_together = (('name', 'environment'), ('uid',))
        managed = True

    def set_attribute(self, key, value=None, update_if_existing=True):
        attrib, created = self.attributes.get_or_create(key=key)
        if not created and not update_if_existing:
            raise FeatureToggleAttributeAlreadyExists(**dict(key=key))

        attrib.value = value
        attrib.save()

    def get_attribute(self, key, raise_does_not_exist=False):
        try:
            attr = self.attributes.get(key=key)
            return attr.value
        except ObjectDoesNotExist:
            if raise_does_not_exist:
                FeatureToggleAttributeDoesNotExist(**dict(key=key))
            return None

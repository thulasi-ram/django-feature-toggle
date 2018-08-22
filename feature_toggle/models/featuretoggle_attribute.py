# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from djutil.models import TimeStampedModel

from constants import Attributes
from feature_toggle.models.featuretoggle import FeatureToggle
from utilities import django_model_choices_from_iterable

CHOICES = django_model_choices_from_iterable(getattr(settings, 'FEATURE_TOGGLE_ATTR_CHOICES', Attributes))


class FeatureToggleAttribute(TimeStampedModel):
    key_max_length = getattr(settings, 'FEATURE_TOGGLE_ATTRIB_KEY_MAX_LEN', 100)
    val_max_length = getattr(settings, 'FEATURE_TOGGLE_ATTRIB_VAL_MAX_LEN', 1000)

    feature_toggle = models.ForeignKey(FeatureToggle, related_name='attributes', on_delete=models.CASCADE)
    key = models.CharField(max_length=key_max_length, choices=CHOICES)
    value = models.TextField(max_length=val_max_length, null=True, blank=True)

    class Meta:
        unique_together = ('feature_toggle', 'key')
        managed = False

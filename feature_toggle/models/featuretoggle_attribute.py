# -*- coding: utf-8 -*-

from django.db import models
from djutil.models import TimeStampedModel

from feature_toggle import constants
from feature_toggle.models.featuretoggle import FeatureToggle


class FeatureToggleAttribute(TimeStampedModel):
    feature_toggle = models.ForeignKey(FeatureToggle, related_name='attributes')
    key = models.CharField(max_length=constants.FeatureToggle.Attributes.DEFAULT_FT_ATTRIBUTE_KEY_LENGTH,
                           choices=constants.FeatureToggle.Attributes.CHOICES)
    value = models.TextField(max_length=constants.FeatureToggle.Attributes.DEFAULT_FT_ATTRIBUTE_VALUE_LENGTH,
                             null=True,
                             blank=True)

    class Meta:
        unique_together = ('feature_toggle', 'key')

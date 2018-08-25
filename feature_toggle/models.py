# -*- coding: utf-8 -*-


from django.conf import settings
from django.db import models
from djutil.models import TimeStampedModel

from feature_toggle.exceptions import FeatureToggleAttributeAlreadyExists
from .constants import Environments, Attributes
from .utilities import django_model_choices_from_iterable, make_meanigful_id

ENV_CHOICES = django_model_choices_from_iterable(Environments)
ATTRIB_CHOICES = django_model_choices_from_iterable(Attributes)

ATTRIB_KEY_MAX_LENGTH = getattr(settings, 'FEATURE_TOGGLE_ATTRIB_KEY_MAX_LEN', 100)
ATTRIB_VAL_MAX_LENGTH = getattr(settings, 'FEATURE_TOGGLE_ATTRIB_VAL_MAX_LEN', 1000)


class FeatureToggle(TimeStampedModel):
    uid = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    environment = models.CharField(max_length=50, choices=ENV_CHOICES)
    is_active = models.BooleanField(default=True)
    start_date_time = models.DateTimeField(auto_now_add=True)
    end_date_time = models.DateTimeField(auto_now_add=True)  # todo: add 3 months from now by default
    time_bomb = models.BooleanField(default=False)

    class Meta:
        unique_together = (('name', 'environment'), ('uid',))
        managed = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.uid:
            self.uid = make_meanigful_id(self.name, length=5)
        super().save(force_insert, force_update, using, update_fields)

    def set_attribute(self, key, value=None, update_if_existing=True):
        attrib, created = self.attributes.get_or_create(key=key)
        if not created and not update_if_existing:
            raise FeatureToggleAttributeAlreadyExists(**dict(key=key))

        attrib.value = value
        attrib.save()

    def __str__(self):
        return "{e}: {n}({u})".format(e=self.environment, n=self.name, u=self.uid)

    def __unicode__(self):
        return self.__str__()


class FeatureToggleAttribute(TimeStampedModel):
    feature_toggle = models.ForeignKey(FeatureToggle, related_name='attributes', on_delete=models.CASCADE)
    key = models.CharField(max_length=ATTRIB_KEY_MAX_LENGTH, choices=ATTRIB_CHOICES)
    value = models.TextField(max_length=ATTRIB_VAL_MAX_LENGTH, null=True, blank=True)

    class Meta:
        unique_together = ('feature_toggle', 'key')
        managed = False

    def __str__(self):
        return "{ft}: {k} - {v}".format(ft=str(self.feature_toggle), k=self.key, v=self.value)

    def __unicode__(self):
        return self.__str__()

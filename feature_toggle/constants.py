# -*- coding: utf-8 -*-
from django.conf import settings


class FeatureToggle(object):
    date_format = '%Y-%m-%d'

    class Environment:
        LOCAL = 'local'
        DEV = 'dev'
        PREPROD = 'preprod'
        PROD = 'prod'

        _default_choices = tuple([(x, x) for x in [LOCAL, DEV, PREPROD, PROD]])

        DEFAULT_CHOICES = getattr(settings, 'FEATURE_TOGGLE_DEFAULT_ENV_CHOICES', _default_choices)

        CUSTOM_CHOICES = getattr(settings, 'FEATURE_TOGGLE_CUSTOM_ENV_CHOICES', ())

        try:
            CHOICES = DEFAULT_CHOICES + CUSTOM_CHOICES
        except TypeError:
            raise RuntimeError("Default/Custom Choices for environments should be a tuple of tuple")

    class Attributes:
        DEFAULT_FT_ATTRIBUTE_KEY_LENGTH = 100
        DEFAULT_FT_ATTRIBUTE_VALUE_LENGTH = 1000

        MODULE = 'module'
        START_DATE = 'start_date'
        END_DATE = 'end_date'
        TIME_BOMB = 'time_bomb'

        _default_choices = tuple([(x, x) for x in [MODULE, START_DATE, END_DATE, TIME_BOMB]])

        DEFAULT_CHOICES = getattr(settings, 'FEATURE_TOGGLE_DEFAULT_ATTR_CHOICES', _default_choices)

        CUSTOM_CHOICES = getattr(settings, 'FEATURE_TOGGLE_CUSTOM_ATTR_CHOICES', ())

        try:
            CHOICES = DEFAULT_CHOICES + CUSTOM_CHOICES
        except TypeError:
            raise RuntimeError("Default/Custom choices for attributes must be an iterable containing "
                               "(actual value, human readable name) tuples.")

# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .utilities import Container


# pylint: disable=invalid-name
class Attribute(Container):
    Module = 'module'

    Default = [
        Module,
    ]

    try:
        Custom = getattr(settings, 'FEATURE_TOGGLE_ATTR_CHOICES', None)
    except ImproperlyConfigured:
        # for unittests
        Custom = None

    def __init__(self):
        super().__init__(self.Custom or self.Default)


# pylint: disable=invalid-name
class Environment(Container):
    Local = 'local'
    Dev = 'dev'
    Preprod = 'preprod'
    Prod = 'prod'

    Default = [
        Local,
        Dev,
        Preprod,
        Prod,
    ]

    try:
        Custom = getattr(settings, 'FEATURE_TOGGLE_ENV_CHOICES', None)
    except ImproperlyConfigured:
        # for unittests
        Custom = None

    def __init__(self):
        super().__init__(self.Custom or self.Default)


Environments = Environment()
Attributes = Attribute()

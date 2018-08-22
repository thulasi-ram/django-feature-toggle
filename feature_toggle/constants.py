# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from utilities import Container


class Environment:
    LOCAL = 'local'
    DEV = 'dev'
    PREPROD = 'preprod'
    PROD = 'prod'


class Attribute:
    MODULE = 'module'


DefaultEnvironments = [
    Environment.LOCAL,
    Environment.DEV,
    Environment.PREPROD,
    Environment.PROD,
]

DefaultAttributes = [
    Attribute.MODULE,
]


class AttribContainer(Container):
    pass


class EnvContainer(Container):
    pass


Environments = EnvContainer(getattr(settings, 'FEATURE_TOGGLE_ENV_CHOICES', DefaultEnvironments))
Attributes = AttribContainer(getattr(settings, 'FEATURE_TOGGLE_ATTR_CHOICES', DefaultAttributes))

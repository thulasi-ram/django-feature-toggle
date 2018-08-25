# -*- coding: utf-8 -*-


from django.conf import settings

from .utilities import Container


class Attribute(Container):
    Module = 'module'

    Default = [
        Module,
    ]

    Custom = getattr(settings, 'FEATURE_TOGGLE_ATTR_CHOICES', None)

    def __init__(self):
        super().__init__(items=self.Custom or self.Default)


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

    Custom = getattr(settings, 'FEATURE_TOGGLE_ENV_CHOICES', None)

    def __init__(self):
        super().__init__(items=self.Custom or self.Default)


Environments = Environment()
Attributes = Attribute()

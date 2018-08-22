# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from enum import Enum


class Environments(Enum):
    LOCAL = 'local'
    DEV = 'dev'
    PREPROD = 'preprod'
    PROD = 'prod'


class Attributes(Enum):
    MODULE = 'module'

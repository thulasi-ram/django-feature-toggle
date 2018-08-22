# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from feature_toggle.constants import Environments
from feature_toggle.exceptions import FeatureToggleDoesNotExist
from feature_toggle.toggle import BaseToggle
from models import FeatureToggle

logger = logging.getLogger(__name__)


class FeatureToggleService(object):

    @classmethod
    def get_toggle(cls, uid):
        try:
            return FeatureToggle.objects.get(uid=uid)
        except FeatureToggle.DoesNotExist:
            msg = 'Feature Toggle for uid: {u} does not exist.'.format(u=uid)
            raise FeatureToggleDoesNotExist(msg)

    @classmethod
    def get_toggle_from_name_and_env(cls, name, environment):
        assert environment in Environments
        try:
            return FeatureToggle.objects.get(name=name, environment=environment)
        except FeatureToggle.DoesNotExist:
            msg = 'Feature for name: {n} and env: {e} does not exist.'.format(n=name, e=environment)
            raise FeatureToggleDoesNotExist(msg)

    @classmethod
    def create_toggle(cls, toggle):
        assert isinstance(toggle, BaseToggle)
        tgl = FeatureToggle.objects.create(name=toggle.name)
        for key, value in tgl.attributes.items():
            tgl.set_attribute(key, value)

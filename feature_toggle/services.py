# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from feature_toggle.constants import Environments
from feature_toggle.exceptions import FeatureToggleDoesNotExist
from feature_toggle.toggle import BaseToggle, Toggle
from models import FeatureToggle

logger = logging.getLogger(__name__)


class FeatureToggleService(object):

    @classmethod
    def get(cls, uid):
        tgl = cls.get_model(uid)
        return cls.convert(toggle_model=tgl)

    @classmethod
    def create(cls, toggle):
        assert isinstance(toggle, BaseToggle)
        tgl = FeatureToggle.objects.create(name=toggle.name)
        for key, value in tgl.attributes.items():
            tgl.set_attribute(key, value)

    @classmethod
    def get_model(cls, uid):
        try:
            return FeatureToggle.objects.get(uid=uid)
        except FeatureToggle.DoesNotExist:
            msg = 'Feature Toggle for uid: {u} does not exist.'.format(u=uid)
            raise FeatureToggleDoesNotExist(msg)

    @classmethod
    def get_from_name_and_env(cls, name, environment):
        assert environment in Environments
        try:
            tgl = FeatureToggle.objects.get(name=name, environment=environment)
        except FeatureToggle.DoesNotExist:
            msg = 'Feature for name: {n} and env: {e} does not exist.'.format(n=name, e=environment)
            raise FeatureToggleDoesNotExist(msg)

        return cls.convert(toggle_model=tgl)

    @classmethod
    def convert(cls, toggle_model):
        toggle_attributes = toggle_model.attibutes.all().values('key', 'value')
        toggle_attributes = {attrib['key']: attrib['value'] for attrib in toggle_attributes.items()}
        tgl = Toggle(
            uid=toggle_model.uid,
            name=toggle_model.name,
            environment=toggle_model.environment,
            is_active=toggle_model.is_active,
            start_date_time=toggle_model.start_date_time,
            end_date_time=toggle_model.end_date_time,
            time_bomb=toggle_model.time_bomb,
            attributes=toggle_attributes,
        )
        return tgl

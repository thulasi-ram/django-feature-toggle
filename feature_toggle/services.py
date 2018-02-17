# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import logging

from feature_toggle import constants
from feature_toggle.exceptions import FeatureToggleDoesNotExist, FeatureToggleAlreadyExists
from feature_toggle.models.featuretoggle import FeatureToggle
from feature_toggle.utilities import format_to_date

logger = logging.getLogger(__name__)


class FeatureToggleService(object):
    """
    This service is especially to be dealt with Feature Toggles.

    All interfaces to the model is supposed to go through this method.
    """

    @classmethod
    def get_toggle(cls, name, code, env, raise_does_not_exist=True):
        data = dict(name=name, code=code, environment=env, raise_does_not_exist=raise_does_not_exist)
        return cls._get_toggle(**data)

    @classmethod
    def get_toggle_by_name(cls, name, env, raise_does_not_exist=True):
        data = dict(name=name, environment=env, raise_does_not_exist=raise_does_not_exist)
        return cls._get_toggle(**data)

    @classmethod
    def get_toggle_by_code(cls, code, env, raise_does_not_exist=True):
        data = dict(code=code, environment=env, raise_does_not_exist=raise_does_not_exist)
        return cls._get_toggle(**data)

    @classmethod
    def create_toggle(cls, name, code, env, attributes=None):
        """
        Creates a toggle and sets its attributes
        :param name: Name of the toggle
        :param code: Code of the toggle
        :param env: env of the toggle
        :param attributes: Dict of any attributes to be set on the toggle.
        :return: FeatureToggle object
        """
        tgl = cls._create_toggle(**dict(name=name, code=code, environment=env))
        if attributes:
            cls.set_attributes(tgl=tgl, attributes=attributes, update_if_existing=False)
        return tgl

    @classmethod
    def set_attributes(cls, tgl, attributes, update_if_existing):
        assert isinstance(attributes, dict)
        for key, value in attributes.items():
            tgl.set_attribute(key, value, update_if_existing=update_if_existing)

    @classmethod
    def _get_toggle(cls, **kwargs):

        # extracting from kwargs
        env = kwargs.get('environment')
        raise_does_not_exist = kwargs.pop('raise_does_not_exist', True)

        assert any(env in en for en in constants.FeatureToggle.Environment.CHOICES)

        try:
            return FeatureToggle.objects.get(**kwargs)
        except FeatureToggle.DoesNotExist:
            logger.warn('Feature for args: {arg} does not exist.'.format(arg=kwargs))
            if raise_does_not_exist:
                raise FeatureToggleDoesNotExist(**kwargs)
            logger.warn('Suppressing does not exist')
            return FeatureToggle(**kwargs)

    @classmethod
    def _create_toggle(cls, **kwargs):

        if FeatureToggle.objects.filter(**kwargs).exists():
            raise FeatureToggleAlreadyExists(**kwargs)
        return FeatureToggle.objects.create(**kwargs)

    @classmethod
    def is_active(cls, feature_toggle):
        """
        *WARNING*: Only checks for the is_active flag. Ignores start_date and end_date check.
        For complete check see is_enabled
        :param feature_toggle: Object of FeatureToggle
        :return: Boolean
        """
        assert isinstance(feature_toggle, FeatureToggle)
        return feature_toggle.is_active

    @classmethod
    def is_enabled(cls, feature_toggle, validation_date=datetime.datetime.now().date()):
        """
        *WARNING*: Does a complete check if start_date and end_date are present. If they are not present
        the behaviour is similar to is_active method.
        :param feature_toggle: Object of FeatureToggle
        :param validation_date: Date to be validated against to find the status of a Toggle
        :return: Boolean
        """
        assert isinstance(feature_toggle, FeatureToggle)

        try:
            if cls.is_active(feature_toggle):
                start_date, end_date = feature_toggle.start_date, feature_toggle.end_date

                if start_date and end_date:
                    # if both start and end times are present
                    if format_to_date(start_date) <= validation_date <= format_to_date(end_date):
                        return True
                elif start_date:
                    # if only start time is present
                    if format_to_date(start_date) <= validation_date:
                        return True
                elif end_date:
                    # if only end time is present
                    if validation_date <= format_to_date(end_date):
                        return True
                else:
                    # this means both start and end has not been set so we don't do validations
                    return True
        except Exception as e:
            logger.exception(e)
            raise

        return False

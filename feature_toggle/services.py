# -*- coding: utf-8 -*-

import datetime
import logging

from django.conf import settings

from feature_toggle import constants
from feature_toggle.models import FeatureToggle
from feature_toggle.utilities import format_to_date


class FeatureToggleService(object):
    """
    This service is especially to be dealt with Feature Toggles.

    All interfaces to the model is supposed to go through this method.
    """

    @classmethod
    def _get_toggle(cls, **kwargs):
        logger = logging.getLogger(cls.__name__)

        # extracting from kwargs
        env = kwargs.get('environment')
        raise_does_not_exist = kwargs.pop('raise_does_not_exist', True)

        assert any(env in en for en in constants.FeatureToggle.Environment.CHOICES)

        try:
            return FeatureToggle.objects.get(**kwargs)
        except FeatureToggle.DoesNotExist:
            logger.warn('Feature for args: {arg} does not exist.'.format(arg=kwargs))
            if raise_does_not_exist:
                raise
            logger.warn('Suppressing does not exist')
            return FeatureToggle()  # TODO: Should return it initialized with passed values?

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

        logger = logging.getLogger(cls.__name__)

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

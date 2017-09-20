# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist

from feature_toggle.services import FeatureToggleService
from feature_toggle.toggle_base import BaseToggle


class Toggle(BaseToggle):
    """
    Actual toggle class for implementing a toggle.
    """

    raise_does_not_exist = True

    def __init__(self, environment, name=None, code=None, **kwargs):
        self.raise_does_not_exist = kwargs.get('raise_does_not_exist', self.raise_does_not_exist)

        if name and code:
            self._feature_toggle = FeatureToggleService.get_toggle(name=name,
                                                                   code=code,
                                                                   env=environment,
                                                                   raise_does_not_exist=self.raise_does_not_exist)
        elif name:
            self._feature_toggle = FeatureToggleService.get_toggle_by_name(name=name,
                                                                           env=environment,
                                                                           raise_does_not_exist=self.raise_does_not_exist)
        elif code:
            self._feature_toggle = FeatureToggleService.get_toggle_by_code(code=code,
                                                                           env=environment,
                                                                           raise_does_not_exist=self.raise_does_not_exist)
        else:
            raise RuntimeError("Any one of name or code is mandatory")

        self.__fully_initialized__ = True  # should be the last line always

    @property
    def name(self):
        return self._feature_toggle.name

    @property
    def code(self):
        return self._feature_toggle.code

    @property
    def environment(self):
        return self._feature_toggle.environment

    def is_active(self):
        return FeatureToggleService.is_active(self._feature_toggle)

    def is_enabled(self):
        return FeatureToggleService.is_enabled(self._feature_toggle)

    def __getattr__(self, attrib):
        """
        A hook to access FeatureToggleAttributes.
        Returns the attribute value for a given key.
        :return: None, usually should be the value of the attribute
        """

        if attrib == '__fully_initialized__':
            # if in this loop means we have called this method from this method again
            # and we are about to slip into a max recursion error.
            # this can also mean the __fully_initialized__ is not set on the class
            raise AttributeError('__fully_initialized__ does not exist. Implement the sentinel in the class')

        sentinel = '__sentinel__'
        if getattr(self, '__fully_initialized__', sentinel) is sentinel:
            # this check is there to ensure the object is completely initialized before we proceed to access
            # self._feature_toggle. Without that check we will be checking in loop for attribute `_feature_toggle`
            # which will cause max recursion error.

            # We don't proceed until we are sure we have `_feature_toggle` set on our class.
            # Since there is no direct way to do it we resort to the variable  `__fully_initialized__` to be set
            # Hence without __fully_initialized__ the object of this class will loose the ability
            # to directly access FeatureToggleAttributes.

            raise AttributeError(attrib)

        try:
            return self._feature_toggle.get_attribute(key=attrib, raise_does_not_exist=True)  # always to be true
        except ObjectDoesNotExist:
            raise AttributeError(attrib)

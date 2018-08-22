# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import abc


class BaseToggle(object):
    """
    Interface for implementing toggle class
    """

    def __init__(self, uid, name, environment, is_active,
                 start_date=None, end_date=None, time_bomb=None, attributes=None,
                 **kwargs):
        self.uid = uid
        self.name = name
        self.environment = environment
        self.is_active = is_active

        self.start_date = start_date
        self.end_date = end_date
        self.time_bomb = time_bomb

        if attributes:
            assert isinstance(attributes, dict)
            self.attributes = attributes

        self.kwargs = kwargs

    @abc.abstractmethod
    def __bool__(self):
        pass

    __nonzero__ = __bool__


class Toggle(BaseToggle):

    def __bool__(self):
        return self.is_active

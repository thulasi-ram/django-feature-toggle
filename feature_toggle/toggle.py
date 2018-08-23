# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import warnings
from datetime import datetime


class BaseToggle(object):
    """
    Interface for implementing toggle class
    """

    class Attributes(object):
        def __init__(self, attribs):
            assert isinstance(attribs, dict)

            self.attribs = attribs

        def __getattr__(self, item):
            try:
                return self.attribs[item]
            except KeyError:
                raise AttributeError(item)

    def __init__(self, uid, name, environment, is_active, attributes=None, **kwargs):
        self.uid = uid
        self.name = name
        self.environment = environment
        self.is_active = is_active

        if attributes:
            self.attributes = self.Attributes(attributes)

        self.kwargs = kwargs

    def __bool__(self):
        return bool(self.is_active)

    __nonzero__ = __bool__


class Toggle(BaseToggle):
    """
    This is a time bomb toggle by default.

    A time bomb toggle stops working after the end date. Generally toggle's lifetime should be predetermined.
    If not toggles can pollute the code base. A bit of discipline is needed to maintain toggles and time bomb
    helps enforce it.

    This toggle will spit a warning if not time bomb and will get disabled if it is a time bomb.
    i.e., `if toggle` will return false even if it is active
    So don't blame the poor toggle now.

    """

    def __init__(self, uid, name, environment, is_active,
                 start_date_time, end_date_time, time_bomb=True,
                 attributes=None, **kwargs):
        if time_bomb and not (start_date_time or end_date_time):
            raise RuntimeError('Start date and end date is mandatory for a time bomb')
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.time_bomb = time_bomb
        super().__init__(uid, name, environment, is_active, attributes, **kwargs)

    def __bool__(self):
        active = super().__bool__()
        now = datetime.utcnow()

        if not active:
            return False

        if self.end_date_time and self.end_date_time < datetime.utcnow():
            # this check because toggles can quickly get overwhelming
            warnings.warn('{t} has expired. Get rid of me and help me attain salvation')

        if not self.time_bomb:
            return True

        return self.start_date_time <= now <= self.end_date_time

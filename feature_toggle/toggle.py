# -*- coding: utf-8 -*-


import datetime
import warnings

from feature_toggle.constants import Environments
from feature_toggle.utilities import utc_now


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
        assert environment in Environments
        self.environment = environment
        self.is_active = is_active

        if attributes:
            self.attributes = self.Attributes(attributes)

        self.kwargs = kwargs

    def __bool__(self):
        return bool(self.is_active)

    __nonzero__ = __bool__


class Toggle(BaseToggle):

    def __init__(self, uid, name, environment, is_active,
                 start_date_time, end_date_time,
                 attributes=None, **kwargs):
        assert isinstance(start_date_time, datetime.datetime)  # should be a time stamp
        assert start_date_time.tzinfo is not None  # should have a time zone. otherwise causes confusions
        self.start_date_time = start_date_time

        assert isinstance(end_date_time, datetime.datetime)  # should be a time stamp
        assert end_date_time.tzinfo is not None  # should have a time zone. otherwise causes confusions
        self.end_date_time = end_date_time
        super().__init__(uid, name, environment, is_active, attributes, **kwargs)

    def __bool__(self):
        active = super().__bool__()

        if self.end_date_time and self.end_date_time < utc_now():
            # this check because toggles can quickly get overwhelming
            warnings.warn('{t} has expired. Get rid of me and help me attain salvation'.format(t=str(self)))

        return active


class TimeBombToggle(Toggle):
    """
    This is a time bomb toggle by default.

    A time bomb toggle stops working after the end date. Generally toggle's lifetime should be predetermined.
    If not toggles can pollute the code base. A bit of discipline is needed to maintain toggles and time bomb
    helps enforce it.

    This toggle will spit a warning if not time bomb and will get disabled if it is a time bomb.
    i.e., `if toggle` will return false even if it is active
    So don't blame the poor toggle now.

    """

    def __bool__(self):
        active = super().__bool__()

        if active:
            return self.start_date_time <= utc_now() <= self.end_date_time
        return active

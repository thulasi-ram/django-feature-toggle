# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class FeatureToggleDoesNotExist(Exception):
    """
    This exception is to aid consumers in providing an common exception to catch instead of relying on
    model.DoesNotExist.
    """

    def __init__(self, **kwargs):
        msg = 'FeatureToggle cannot be created with data: {d}'.format(d=kwargs)
        super(FeatureToggleDoesNotExist, self).__init__(self, msg)


class FeatureToggleAlreadyExists(Exception):
    """
    This exception is raised at multiple places.
    Eg: when trying to create a toggle that already exists.
    """

    def __init__(self, **kwargs):
        msg = kwargs.pop('msg') if 'msg' in kwargs else ''
        if not msg:
            msg = 'FeatureToggle already exists'
            if kwargs:
                msg += 'for data: {d}'.format(d=kwargs)
        super(FeatureToggleAlreadyExists, self).__init__(self, msg)


class FeatureToggleAttributeDoesNotExist(Exception):
    """
    This exception is to aid consumers in providing an common exception to catch instead of relying on
    model.DoesNotExist for attributes
    """

    def __init__(self, **kwargs):
        msg = 'FeatureToggleAttribute cannot be created with data: {d}'.format(d=kwargs)
        super(FeatureToggleAttributeDoesNotExist, self).__init__(self, msg)


class FeatureToggleAttributeAlreadyExists(Exception):
    """
    Wen trying to create a toggle attribute that already exists.
    """

    def __init__(self, **kwargs):
        msg = 'FeatureToggleAttribute already exists with data: {d}'.format(d=kwargs)
        super(FeatureToggleAttributeAlreadyExists, self).__init__(self, msg)

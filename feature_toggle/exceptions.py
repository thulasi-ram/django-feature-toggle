# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class FeatureToggleDoesNotExist(Exception):
    """
    This exception is to aid consumers in providing an common exception to catch instead of relying on
    model.DoesNotExist.
    """
    pass


class FeatureToggleAlreadyExists(Exception):
    """
    This exception is raised when trying to create a toggle that already exists.
    """
    pass


class FeatureToggleAttributeAlreadyExists(Exception):
    """
    When trying to create a toggle attribute that already exists.
    """

    def __init__(self, **kwargs):
        msg = 'FeatureToggleAttribute already exists with data: {d}'.format(d=kwargs)
        super(FeatureToggleAttributeAlreadyExists, self).__init__(self, msg)

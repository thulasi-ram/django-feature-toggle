# -*- coding: utf-8 -*-
import datetime

from feature_toggle import constants


def format_to_date(date):
    if isinstance(date, datetime.date):
        date = date.strftime(constants.FeatureToggle.date_format)
    elif isinstance(date, basestring):
        date = datetime.datetime.strptime(date, constants.FeatureToggle.date_format).date()
    else:
        raise RuntimeError('Can only accept valid dates/strings')
    return date

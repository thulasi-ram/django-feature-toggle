# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def django_model_choices_from_iterable(iterable):
    try:
        return tuple((x, x) for x in iterable)
    except TypeError:
        raise ValueError("must be an iterable")

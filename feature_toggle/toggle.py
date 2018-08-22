# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from feature_toggle.toggle_base import BaseToggle


class Toggle(BaseToggle):

    def __bool__(self):
        return self.is_active

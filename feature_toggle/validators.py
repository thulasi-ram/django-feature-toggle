# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.core.validators import RegexValidator, _

try:
    from django.core.validators import _lazy_re_compile

    code_re = _lazy_re_compile(r'^[A-Z_]+\Z')
except ImportError:
    code_re = re.compile(r'^[A-Z_]+\Z')

validate_feature_toggle_code = RegexValidator(code_re,
                                              _("Enter a valid 'code' of CAPITAL letters and underscores only."),
                                              'invalid')

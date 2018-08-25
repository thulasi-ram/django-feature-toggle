# -*- coding: utf-8 -*-


from constants import Environments
from feature_toggle.toggle import Toggle


def test_given_simple_active_toggle_when_evaluated_then_returns_true():
    """
    test_case_type: positive
    test_case_complexity: simple
    """
    simple_active_toggle = Toggle(
        uid=1,
        name="test",
        environment=Environments.Local,
        is_active=True,
        start_date_time=None,
        end_date_time=None,
        time_bomb=False
    )
    assert simple_active_toggle is True

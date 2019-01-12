# -*- coding: utf-8 -*-
import datetime
import pytest

from feature_toggle.constants import Environments
from feature_toggle.toggle import BaseToggle, Toggle, TimeBombToggle
from feature_toggle.utilities import utc_now


def test_given_basic_active_toggle_when_evaluated_then_returns_true():
    """
    test_case_type: positive
    test_case_complexity: simple
    """
    simple_active_toggle = BaseToggle(
        uid=1,
        name="test",
        environment=Environments.Local,
        is_active=True,
    )
    assert bool(simple_active_toggle) is True


def test_given_basic_inactive_toggle_when_evaluated_then_returns_false():
    """
    test_case_type: positive
    test_case_complexity: simple
    """
    simple_active_toggle = BaseToggle(
        uid=1,
        name="test",
        environment=Environments.Local,
        is_active=False,
    )
    assert bool(simple_active_toggle) is False


def test_given_basic_toggle_when_given_invalid_environment_then_fails():
    """
    test_case_type: negative
    test_case_complexity: simple
    """
    with pytest.raises(AssertionError):
        BaseToggle(
            uid=1,
            name="test",
            environment='Invalid Environment',
            is_active=False,
        )


def test_given_simple_active_toggle_when_evaluated_then_returns_true():
    """
    test_case_type: positive
    test_case_complexity: simple
    """

    today = utc_now()
    some_far_away_date = today + datetime.timedelta(days=9999)
    simple_active_toggle = Toggle(
        uid=1,
        name="test",
        environment=Environments.Local,
        is_active=True,
        start_date_time=today,
        end_date_time=some_far_away_date,
    )
    assert bool(simple_active_toggle) is True


def test_given_time_bomb_active_toggle_when_evaluated_with_future_end_date_then_returns_true():
    """
    test_case_type: positive
    test_case_complexity: simple
    """

    today = utc_now()
    some_far_away_date = today + datetime.timedelta(days=9999)
    simple_active_toggle = TimeBombToggle(
        uid=1,
        name="test",
        environment=Environments.Local,
        is_active=True,
        start_date_time=today,
        end_date_time=some_far_away_date,
    )
    assert bool(simple_active_toggle) is True

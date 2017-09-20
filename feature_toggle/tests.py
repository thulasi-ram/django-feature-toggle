# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from feature_toggle import constants
from feature_toggle.models import FeatureToggle
from feature_toggle.toggle import Toggle


class TestToggle(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.active_ft_tgl = FeatureToggle.objects.create(name='test1', code='test1',
                                                         environment=constants.FeatureToggle.Environment.LOCAL)
        cls.inactive_ft_tgl = FeatureToggle.objects.create(name='test2', code='test2', is_active=False,
                                                           environment=constants.FeatureToggle.Environment.LOCAL)

    @classmethod
    def tearDownClass(cls):
        FeatureToggle.objects.all().delete()

    def test_toggle_without_name_and_code(self):
        with self.assertRaises(RuntimeError):
            Toggle(environment=constants.FeatureToggle.Environment.LOCAL)

    def test_toggle_with_invalid_environment(self):
        with self.assertRaises(AssertionError):
            Toggle(environment='__invalid__', name=self.active_ft_tgl.name, code=self.active_ft_tgl.code)

    def test_existing_toggle(self):
        ft_tgl = self.active_ft_tgl
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.name, code=ft_tgl.code)
        self._toggle_equality_test(tgl, ft_tgl)

    def test_non_existing_toggle(self):
        with self.assertRaises(ObjectDoesNotExist):
            Toggle(environment=constants.FeatureToggle.Environment.LOCAL, name='-', code='-')

    def test_non_existing_toggle_with_error_suppression(self):
        tgl = Toggle(environment=constants.FeatureToggle.Environment.LOCAL, name='-', code='-',
                     raise_does_not_exist=False)
        self.assertEqual(tgl.name, '')

    def test_existing_toggle_with_name(self):
        ft_tgl = self.active_ft_tgl
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.name)
        self._toggle_equality_test(tgl, ft_tgl)

    def test_non_existing_toggle_with_name_and_error_suppression(self):
        tgl = Toggle(environment=constants.FeatureToggle.Environment.LOCAL, name='-', raise_does_not_exist=False)
        self.assertEqual(tgl.name, '')

    def test_existing_toggle_with_code(self):
        ft_tgl = self.inactive_ft_tgl
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.code)
        self._toggle_equality_test(tgl, ft_tgl)

    def test_non_existing_toggle_with_code_and_error_suppression(self):
        tgl = Toggle(environment=constants.FeatureToggle.Environment.LOCAL, code='-', raise_does_not_exist=False)
        self.assertEqual(tgl.code, '')

    def test_is_active_with_active_toggle(self):
        ft_tgl = self.active_ft_tgl
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.name, code=ft_tgl.code)
        self.assertTrue(tgl.is_active())

    def test_is_active_with_inactive_toggle(self):
        ft_tgl = self.inactive_ft_tgl
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.name, code=ft_tgl.code)
        self.assertFalse(tgl.is_active())

    def test_is_enabled_with_start_date_less_than_now(self):
        yesterday = datetime.date.today() - datetime.timedelta(1)
        ft_tgl = self.active_ft_tgl
        ft_tgl.set_attribute(constants.FeatureToggle.Attributes.START_DATE, yesterday)
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.name, code=ft_tgl.code)
        self.assertTrue(tgl.is_enabled())

    def test_is_enabled_with_start_date_greater_than_now(self):
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        ft_tgl = self.active_ft_tgl
        ft_tgl.set_attribute(constants.FeatureToggle.Attributes.START_DATE, tomorrow)
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.name, code=ft_tgl.code)
        self.assertFalse(tgl.is_enabled())

    def test_is_enabled_with_end_date_less_than_now(self):
        yesterday = datetime.date.today() - datetime.timedelta(1)
        ft_tgl = self.active_ft_tgl
        ft_tgl.set_attribute(constants.FeatureToggle.Attributes.END_DATE, yesterday)
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.name, code=ft_tgl.code)
        self.assertFalse(tgl.is_enabled())

    def test_is_enabled_with_end_date_greater_than_now(self):
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        ft_tgl = self.active_ft_tgl
        ft_tgl.set_attribute(constants.FeatureToggle.Attributes.END_DATE, tomorrow)
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.name, code=ft_tgl.code)
        self.assertTrue(tgl.is_enabled())

    def test_is_enabled_with_active_toggle_with_both_start_and_end_date_for_valid_range(self):
        yesterday = datetime.date.today() - datetime.timedelta(1)
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        ft_tgl = self.active_ft_tgl
        ft_tgl.set_attribute(constants.FeatureToggle.Attributes.START_DATE, yesterday)
        ft_tgl.set_attribute(constants.FeatureToggle.Attributes.END_DATE, tomorrow)
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.name, code=ft_tgl.code)
        self.assertTrue(tgl.is_enabled())

    def test_is_enabled_with_active_toggle_with_both_start_and_end_date_for_invalid_range(self):
        yesterday = datetime.date.today() - datetime.timedelta(1)
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        ft_tgl = self.active_ft_tgl
        ft_tgl.set_attribute(constants.FeatureToggle.Attributes.START_DATE, tomorrow)
        ft_tgl.set_attribute(constants.FeatureToggle.Attributes.END_DATE, yesterday)
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.name, code=ft_tgl.code)
        self.assertFalse(tgl.is_enabled())

    def test_is_enabled_with_inactive_toggle_without_date(self):
        ft_tgl = self.inactive_ft_tgl
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.name, code=ft_tgl.code)
        self.assertFalse(tgl.is_enabled())

    def test_is_enabled_with_inactive_toggle_with_start_date(self):
        yesterday = datetime.date.today() - datetime.timedelta(1)
        ft_tgl = self.inactive_ft_tgl
        ft_tgl.set_attribute(constants.FeatureToggle.Attributes.START_DATE, yesterday)
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.name, code=ft_tgl.code)
        self.assertFalse(tgl.is_enabled())

    def test_is_enabled_with_inactive_toggle_with_end_date(self):
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        ft_tgl = self.inactive_ft_tgl
        ft_tgl.set_attribute(constants.FeatureToggle.Attributes.END_DATE, tomorrow)
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.name, code=ft_tgl.code)
        self.assertFalse(tgl.is_enabled())

    def test_is_enabled_with_inactive_toggle_with_both_start_and_end_date(self):
        yesterday = datetime.date.today() - datetime.timedelta(1)
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        ft_tgl = self.inactive_ft_tgl
        ft_tgl.set_attribute(constants.FeatureToggle.Attributes.START_DATE, yesterday)
        ft_tgl.set_attribute(constants.FeatureToggle.Attributes.END_DATE, tomorrow)
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.name, code=ft_tgl.code)
        self.assertFalse(tgl.is_enabled())

    def test_is_attribute_of_a_toggle(self):
        time_bomb = '__time_bomb__'
        ft_tgl = self.active_ft_tgl
        ft_tgl.set_attribute(constants.FeatureToggle.Attributes.TIME_BOMB, time_bomb)
        tgl = Toggle(environment=ft_tgl.environment, name=ft_tgl.name, code=ft_tgl.code)
        self.assertEquals(getattr(tgl, constants.FeatureToggle.Attributes.TIME_BOMB), time_bomb)

    def _toggle_equality_test(self, tgl, ft_tgl):
        self.assertEqual(tgl.code, ft_tgl.code)
        self.assertEqual(tgl.name, ft_tgl.name)
        self.assertEqual(tgl.environment, ft_tgl.environment)
        self.assertEqual(tgl.is_active(), ft_tgl.is_active)

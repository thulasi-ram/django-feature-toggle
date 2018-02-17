# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from feature_toggle.models.featuretoggle import FeatureToggle
from feature_toggle.models.featuretoggle_attribute import FeatureToggleAttribute


class FeatureToggleAttributesAdminInline(admin.TabularInline):
    model = FeatureToggleAttribute
    extra = 0
    min_num = 1


class FeatureToggleAdmin(admin.ModelAdmin):
    inlines = [FeatureToggleAttributesAdminInline]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(FeatureToggleAdmin, self).get_readonly_fields(request, obj)
        if obj:
            readonly_fields += ('code',)
        return readonly_fields


admin.site.register(FeatureToggle, FeatureToggleAdmin)

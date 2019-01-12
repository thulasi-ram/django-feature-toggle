# -*- coding: utf-8 -*-


from django.contrib import admin

from .models import FeatureToggleAttribute, FeatureToggle


class FeatureToggleAttributesAdminInline(admin.TabularInline):
    model = FeatureToggleAttribute
    extra = 0
    min_num = 1


class FeatureToggleAdmin(admin.ModelAdmin):
    inlines = [FeatureToggleAttributesAdminInline]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            readonly_fields += ('uid',)
        return readonly_fields


admin.site.register(FeatureToggle, FeatureToggleAdmin)

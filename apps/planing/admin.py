from django.contrib import admin
from .models import PlaningFeature, Planing


@admin.register(Planing)
class PlaningAdmin(admin.ModelAdmin):
    pass


@admin.register(PlaningFeature)
class PlaningFeatureAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin

from .models import Check


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('type', 'status', 'printer',)
    list_filter = ('type', 'status', 'printer',)

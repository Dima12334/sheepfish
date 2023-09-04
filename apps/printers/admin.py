from django.contrib import admin

from .models import Printer


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'check_type', 'point_id',)

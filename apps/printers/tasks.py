from celery import shared_task
from django.db.models import Prefetch

from apps.checks.models import StatusChoices, Check
from .models import Printer


@shared_task
def print_rendered_checks(printer_pks=None):
    """
    :param printer_pks: list of models.Printer pk
    """
    printers = Printer.objects.prefetch_related(
        Prefetch("checks", queryset=Check.objects.filter(status=StatusChoices.RENDERED))
    )
    if printer_pks is not None and len(printer_pks) > 0:
        printers = printers.filter(pk__in=printer_pks)

    for printer in printers:
        for check in printer.checks.all():
            printer.print_check(check)

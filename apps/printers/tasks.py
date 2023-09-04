from celery import shared_task
from django.db.models import Prefetch

from apps.checks.models import StatusChoices, Check
from .models import Printer


@shared_task
def print_rendered_checks():
    printers = Printer.objects.prefetch_related(
        Prefetch("checks", queryset=Check.objects.filter(status=StatusChoices.RENDERED))
    )
    for printer in printers:
        for check in printer.checks.all():
            printer.print_check(check)

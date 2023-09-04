from django.shortcuts import get_object_or_404
from celery import shared_task

from .models import Check, StatusChoices
from .utils import html_to_pdf


@shared_task
def create_pdf_file(check_pk):
    check = get_object_or_404(Check, pk=check_pk)
    file = html_to_pdf(check)
    file_name = f"pdf/{check.order_number}_{check.type}.pdf"

    check.pdf_file.save(file_name, file)
    check.status = StatusChoices.RENDERED
    check.save()

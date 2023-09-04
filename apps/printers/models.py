from django.db import models

from ..checks.models import StatusChoices, CheckTypeChoices


class Printer(models.Model):
    name = models.CharField(verbose_name='Printer name', max_length=255)
    api_key = models.CharField(verbose_name='API key', max_length=35, unique=True)
    check_type = models.CharField(verbose_name='Check type', max_length=7, choices=CheckTypeChoices.choices)
    point_id = models.IntegerField(verbose_name='Point to which the printer is bound')

    def __str__(self):
        return f'Printer {self.name}'

    @staticmethod
    def print_check(check):
        check.status = StatusChoices.PRINTED
        check.save()

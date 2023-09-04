from django.db import models


class CheckTypeChoices(models.TextChoices):
    KITCHEN = "kitchen", "Kitchen"
    CLIENT = "client", "Client"


class StatusChoices(models.TextChoices):
    NEW = "new", "New"
    RENDERED = "rendered", "Rendered"
    PRINTED = "printed", "Printed"


class Check(models.Model):
    printer = models.ForeignKey("printers.Printer", verbose_name="Printer", on_delete=models.CASCADE,
                                related_name="checks")
    type = models.CharField(verbose_name="Check type", max_length=7, choices=CheckTypeChoices.choices)
    order = models.JSONField(verbose_name="Information about order")
    status = models.CharField(verbose_name="Check status", max_length=8, choices=StatusChoices.choices,
                              default=StatusChoices.NEW)
    pdf_file = models.FileField(verbose_name="Check-PDF file", null=True, blank=True)

    def __str__(self):
        return f'Check type "{self.type}"'

    @property
    def order_number(self):
        return self.order[0].get("number")

    @property
    def order_dishes(self):
        return self.order[0].get("dishes", [])

    @property
    def order_sum(self):
        return sum(dish.get("sum", 0) for dish in self.order[0].get("dishes", []))

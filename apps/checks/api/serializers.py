from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import Check
from ..tasks import create_pdf_file
from apps.printers.api.serializers import PrinterSerializer
from apps.printers.models import Printer


class CheckSerializer(serializers.ModelSerializer):
    printer = PrinterSerializer(read_only=True)
    point_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Check
        fields = ("pk", "type", "status", "printer", "order", "point_id")
        read_only_fields = ("pk",)

    def create(self, validated_data):
        point_id = validated_data.pop("point_id")
        check_type = validated_data["type"]
        order_number = validated_data["order"][0].get("number")

        printers = Printer.objects.filter(point_id=point_id, check_type=check_type)

        if not printers:
            error = "There are no printers at this point"
            raise ValidationError({"error": error})
        if Check.objects.filter(order__0__number=order_number, type=check_type).count() > 0:
            error = f"Check already exists. Order number: {order_number}"
            raise ValidationError({"error": error})

        with transaction.atomic():
            checks_to_create = [Check(printer=printer, **validated_data) for printer in printers]
            Check.objects.bulk_create(checks_to_create)

            for check in checks_to_create:
                create_pdf_file.delay(check.pk)

        return {}

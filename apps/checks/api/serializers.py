from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import Check, CheckTypeChoices
from ..tasks import create_pdf_file
from apps.printers.api.serializers import PrinterSerializer
from apps.printers.models import Printer


class CheckSerializer(serializers.ModelSerializer):
    printer = PrinterSerializer(read_only=True)

    class Meta:
        model = Check
        fields = ("pk", "type", "status", "printer", "order")
        read_only_fields = ("pk",)


class CreateCheckSerializer(serializers.ModelSerializer):
    point_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Check
        fields = ("pk", "status", "order", "point_id")
        read_only_fields = ("pk",)

    def create(self, validated_data):
        point_id = validated_data.pop("point_id")
        order_number = validated_data["order"][0].get("number")

        def _create_checks_by_type(check_type):
            printers = Printer.objects.filter(point_id=point_id, check_type=check_type)

            if not printers:
                error = f"There are no {check_type} printers at this point"
                raise ValidationError({"error": error})
            if Check.objects.filter(order__0__number=order_number, type=check_type).count() > 0:
                error = f"Check already exists. Order number: {order_number}"
                raise ValidationError({"error": error})

            checks_to_create = [Check(printer=printer,  type=check_type, **validated_data) for printer in printers]
            Check.objects.bulk_create(checks_to_create)

            for check in checks_to_create:
                create_pdf_file.delay(check.pk)

        with transaction.atomic():
            _create_checks_by_type(CheckTypeChoices.KITCHEN)
            _create_checks_by_type(CheckTypeChoices.CLIENT)

        return {}

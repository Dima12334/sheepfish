from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import PrinterSerializer
from ..models import Printer
from ...base import mixins


class PrinterViewSet(mixins.PermissionPerActionMixin, viewsets.ModelViewSet):
    http_method_names = ("get", "post",)
    serializer_class = PrinterSerializer
    queryset = Printer.objects.all().order_by('pk')
    permission_classes_by_action = {
        "create": (IsAuthenticated,),
        "retrieve": (IsAuthenticated,),
        "list": (IsAuthenticated,),
    }

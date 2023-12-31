from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import CheckSerializer, CreateCheckSerializer
from ..models import Check
from ...base import mixins


class CheckViewSet(mixins.PermissionPerActionMixin, mixins.SerializerPerActionMixin, viewsets.ModelViewSet):
    http_method_names = ("get", "post",)
    serializer_classes_by_action = {
        "create": CreateCheckSerializer,
        "retrieve": CheckSerializer,
        "list": CheckSerializer,
    }
    permission_classes_by_action = {
        "create": (IsAuthenticated,),
        "retrieve": (IsAuthenticated,),
        "list": (IsAuthenticated,),
    }

    def get_queryset(self):
        return Check.objects.select_related("printer").order_by('pk')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({}, status=status.HTTP_201_CREATED)

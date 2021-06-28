from rest_framework import mixins
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet

from store.models import Product, Customer
from store.serializers import ProductSerializer


class ProductViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

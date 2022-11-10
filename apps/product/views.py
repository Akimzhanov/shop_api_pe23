from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response



from .serializers import (
    ProductSerializer,
    ProductListSerializer,
    CategorySerializer
)

from .models import (
    Product,
    ProductImage,
    Category
)



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    # serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    # def get_queryset(self):           #TODO
    #     return Product.objects.all()


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


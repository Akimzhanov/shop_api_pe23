from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


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

    @method_decorator(cache_page(60*15))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    def get_serializer_context(self):            # данные о запросе, (типа откого прилетел запрос)
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_permissions(self):        # 
        if self.action == 'create':
            self.permission_classes == [IsAuthenticated]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):  # каждый раз когда будут просматривать какой то пост, то у него каждый раз повышается на 1
        instance: Product = self.get_object()
        instance.views_count += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)


    # def get_queryset(self):           #TODO
    #     return Product.objects.all()


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer

# Create your views here.

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_object(self):
        lookup_value = self.kwargs[self.lookup_field]
        try:
            # Önce slug ile ara
            return Product.objects.get(slug=lookup_value)
        except Product.DoesNotExist:
            # Bulamazsa main_title ile ara (backward compatibility)
            return Product.objects.get(main_title=lookup_value)

@api_view(['GET'])
def product_list(request):
    """
    List all products
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, slug):
    """
    Retrieve a specific product by slug or main_title
    """
    try:
        # Önce slug ile ara
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        try:
            # Bulamazsa main_title ile ara
            product = Product.objects.get(main_title=slug)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
    
    serializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data)

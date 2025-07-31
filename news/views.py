from django.shortcuts import render
from rest_framework import generics
from .models import News
from .serializers import NewsSerializer

# Create your views here.

class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all().prefetch_related('additional_images')
    serializer_class = NewsSerializer

class NewsDetailAPIView(generics.RetrieveAPIView):
    queryset = News.objects.all().prefetch_related('additional_images')
    serializer_class = NewsSerializer

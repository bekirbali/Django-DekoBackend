from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Class-based views
    path('', views.ProductListAPIView.as_view(), name='product-list'),
    path('<str:main_title>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
    
    # Function-based views (alternative)
    path('list/', views.product_list, name='product-list-func'),
    path('detail/<str:title>/', views.product_detail, name='product-detail-func'),
] 
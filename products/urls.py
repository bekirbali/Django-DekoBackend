from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Class-based views
    path('', views.ProductListAPIView.as_view(), name='product-list'),
    path('<slug:slug>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
    
    # Function-based views (alternative)
    path('list/', views.product_list, name='product-list-func'),
    path('detail/<slug:slug>/', views.product_detail, name='product-detail-func'),
] 
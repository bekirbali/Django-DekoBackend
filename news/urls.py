from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListAPIView.as_view(), name='news-list'),
    path('<int:pk>/', views.NewsDetailAPIView.as_view(), name='news-detail'),
] 
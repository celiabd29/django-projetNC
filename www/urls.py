from django.urls import path
from . import views

urlpatterns = [
    path('', views.site_list, name='home'),
    path('sites/', views.site_list, name='site_list'),
    path('sites/<int:ndegpoi>/', views.site_detail, name='site_detail'),
]

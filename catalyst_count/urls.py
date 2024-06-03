"""
URL configuration for catalyst_count project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from count_app import views, views_api

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/upload_data/', views.upload_data, name='upload_data'),
    path('accounts/query_builder/', views.query_builder, name='query_builder'),
    path('accounts/list_users/', views.list_users, name='list_users'),
    path('accounts/logout/', views.custom_logout, name='custom_logout'),
    path('api/get_query_count', views_api.get_query_count, name='get_query_count'),
]

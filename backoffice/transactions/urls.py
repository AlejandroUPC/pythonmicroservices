"""backoffice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from .views import TransactionViewSet, CustomerAPIView, createUser

urlpatterns = [
    path('transactions', TransactionViewSet.as_view({
        'get':'list'
        
    })),
    path('transactions/<str:customer_id>',TransactionViewSet.as_view({
        'post':'create',
    })),
     path('transactions/<str:_id>', TransactionViewSet.as_view({
        'get':'retrieve',
        'delete': 'remove',
        
    })),
    path('customer/<str:customer_id>', CustomerAPIView.as_view({
        'get':'get_user',
        'post':'create_user'
    })),
]

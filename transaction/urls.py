"""newtender_opertable URL Configuration

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
from django.urls import path
from . import views

urlpatterns = [
    path(
        route='external/create/',
        view=views.ExternalTransactionCreate.as_view(),
        name='external_transaction_create_url'),
    path(
        route='external/dashboard/',
        view=views.ExternalTransactionDashboard.as_view(),
        name='external_transaction_dashboard_url'),
    path(
        route='external/<int:id>/update/',
        view=views.ExternalTransactionUpdate.as_view(),
        name='external_transaction_update_url'),
    path(
        route='external/<int:id>/delete/',
        view=views.ExternalTransactionDelete.as_view(),
        name='external_transaction_delete_url'),
    path(
        route='external/<int:id>/',
        view=views.ExternalTransactionDetails.as_view(),
        name='external_transaction_details_url'),
    path(
        route='internal/create/',
        view=views.InternalTransactionCreate.as_view(),
        name='internal_transaction_create_url'),
    path(
        route='internal/dashboard/',
        view=views.InternalTransactionDashboard.as_view(),
        name='internal_transaction_dashboard_url'),
    path(
        route='internal/<int:id>/update/',
        view=views.InternalTransactionUpdate.as_view(),
        name='internal_transaction_update_url'),
    path(
        route='internal/<int:id>/delete/',
        view=views.InternalTransactionDelete.as_view(),
        name='internal_transaction_delete_url'),
    path(
        route='internal/<int:id>/',
        view=views.InternalTransactionDetails.as_view(),
        name='internal_transaction_details_url'),
    path(
        route='statistic/',
        view=views.StatisticView.as_view(),
        name='statistic_url')
]

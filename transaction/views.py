from django.views.generic import View
from django.shortcuts import render
from .forms import TransactionForm, InternalTransactionForm
from .models import Transaction, InternalTransaction
from .utils import (
    TransactionDetails,
    TransactionDashboard,
    TransactionCreate,
    TransactionUpdate,
    TransactionDelete)


# External transactions views
class ExternalTransactionDetails(TransactionDetails, View):
    model = Transaction
    template = 'external_transaction/details.html'


class ExternalTransactionDashboard(TransactionDashboard, View):
    model = Transaction
    filter_fields = ['author']
    template = 'external_transaction/dashboard.html'


class ExternalTransactionCreate(TransactionCreate, View):
    form = TransactionForm
    template = 'external_transaction/create.html'
    context = {
            'title': 'Создать новую операцию',
            'form_legend': 'Новая операция',
        }


class ExternalTransactionUpdate(TransactionUpdate, View):
    form = TransactionForm
    model = Transaction
    context = {
        'title': 'Изменить операцию',
        'form_legend': 'Изменить операцию',
    }
    template = 'external_transaction/update.html'


class ExternalTransactionDelete(TransactionDelete, View):
    model = Transaction
    template = 'external_transaction/delete.html'
    context = {
        'title': 'Удалить операцию',
        'form_legend': 'Удалить операцию'
    }
    success_url = 'external_transaction_dashboard_url'


# Internal transactions views
class InternalTransactionDetails(TransactionDetails, View):
    model = InternalTransaction
    template = 'internal_transaction/details.html'


class InternalTransactionDashboard(TransactionDashboard, View):
    model = InternalTransaction
    filter_fields = ['donor_user', 'recipient_user']
    template = 'internal_transaction/dashboard.html'


class InternalTransactionCreate(TransactionCreate, View):
    form = InternalTransactionForm
    template = 'internal_transaction/create.html'
    initial_fields = ['donor_user', 'recipient_user']
    context = {
            'title': 'Создать новый внутренний перевод',
            'form_legend': 'Новый внутренний перевод',
        }


class InternalTransactionUpdate(TransactionUpdate, View):
    form = InternalTransactionForm
    model = InternalTransaction
    context = {
        'title': 'Изменить операцию',
        'form_legend': 'Изменить операцию',
    }
    template = 'internal_transaction/update.html'


class InternalTransactionDelete(TransactionDelete, View):
    model = InternalTransaction
    template = 'internal_transaction/delete.html'
    context = {
        'title': 'Удалить операцию',
        'form_legend': 'Удалить операцию'
    }
    success_url = 'internal_transaction_dashboard_url'


class Statistic(View):
    def get(self, request):
        return render(
            request, 'statistic.html', context={'info': 'В разработке'})

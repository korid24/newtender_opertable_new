from datetime import timedelta
from django.views.generic import (View, ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import TransactionForm, InternalTransactionForm, StatisticForm
from .models import Transaction, InternalTransaction
from .services.statistic import Statistic


# External transactions views
class ExternalTransactionDetails(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'external_transaction/details.html'
    context_object_name = 'transaction'
    pk_url_kwarg = 'id'


class ExternalTransactionDashboard(LoginRequiredMixin, ListView):
    template_name = 'external_transaction/dashboard.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        request = self.request
        return request.user.transactions.all()


class ExternalTransactionCreate(LoginRequiredMixin, CreateView):
    form_class = TransactionForm
    model = Transaction
    template_name = 'external_transaction/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ExternalTransactionCreate, self).form_valid(form)


class ExternalTransactionUpdate(LoginRequiredMixin, UpdateView):
    form_class = TransactionForm
    model = Transaction
    template_name = 'external_transaction/update.html'
    pk_url_kwarg = 'id'


class ExternalTransactionDelete(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'external_transaction/delete.html'
    context_object_name = 'transaction'
    success_url = reverse_lazy('external_transaction_dashboard_url')
    pk_url_kwarg = 'id'


# Internal transactions views
class InternalTransactionDetails(LoginRequiredMixin, DetailView):
    model = InternalTransaction
    template_name = 'internal_transaction/details.html'
    context_object_name = 'transaction'
    pk_url_kwarg = 'id'


class InternalTransactionDashboard(LoginRequiredMixin, ListView):
    template_name = 'internal_transaction/dashboard.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        request = self.request
        return (request.user.internal_write_offs.all() |
                request.user.internal_receipts.all())


class InternalTransactionCreate(LoginRequiredMixin, CreateView):
    form_class = InternalTransactionForm
    model = InternalTransaction
    template_name = 'internal_transaction/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(InternalTransactionCreate, self).form_valid(form)

    def get_initial(self):
        user = self.request.user
        return {'donor_user': user, 'recipient_user': user}


class InternalTransactionUpdate(LoginRequiredMixin, UpdateView):
    form_class = InternalTransactionForm
    model = InternalTransaction
    template_name = 'internal_transaction/update.html'
    pk_url_kwarg = 'id'


class InternalTransactionDelete(LoginRequiredMixin, DeleteView):
    model = InternalTransaction
    template_name = 'internal_transaction/delete.html'
    context_object_name = 'transaction'
    success_url = reverse_lazy('internal_transaction_dashboard_url')
    pk_url_kwarg = 'id'


class StatisticView(LoginRequiredMixin, View):
    '''
    Collects data to generate statistics and shows it to the user
    '''
    def get(self, request):
        context = {
            'form': StatisticForm(initial={
                'user': request.user,
                'begin_date': timezone.now() - timedelta(days=31),
                'end_date': timezone.now()
            })
            }
        return render(
            request, 'statistic.html', context=context)

    def post(self, request):
        bound_form = StatisticForm(data=request.POST)
        context = {
            'form': bound_form
        }
        if bound_form.is_valid():
            context['statistic'] = Statistic(**bound_form.cleaned_data)
        return render(request, 'statistic.html', context=context)

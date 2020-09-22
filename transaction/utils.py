from django.shortcuts import render, redirect, reverse, get_object_or_404


class TransactionDetails:
    '''Mixin for transaction details views'''
    model = None
    template = None

    def get(self, request, id):
        current_transaction = get_object_or_404(self.model, id=id)
        context = {
            'title': 'Детали операции',
            'transaction': current_transaction
        }
        return render(request, self.template, context=context)


class TransactionDashboard:
    '''Mixin for transaction dashboards views'''
    model = None
    filter_fields = None
    template = None

    def get(self, request):
        query = self.model.objects.none()
        for field in self.filter_fields:
            query = (query |
                     self.model.objects.filter(**{field: request.user}))
        context = {
            'title': 'Мои операции',
            'transactions': query.order_by('-date', '-id')
        }
        return render(request, self.template, context=context)


class TransactionCreate:
    '''Mixin for transaction create views'''
    form = None
    template = None
    initial_fields = []
    context = None

    def get(self, request):
        initial = {}
        for field in self.initial_fields:
            initial[field] = request.user
        self.context['form'] = self.form(initial=initial)
        return render(request, self.template, context=self.context)

    def post(self, request):
        bound_form = self.form(request.POST)
        self.context['form'] = bound_form
        if bound_form.is_valid():
            new_transaction = bound_form.save(commit=False)
            new_transaction.author = request.user
            new_transaction.save()
            return redirect(new_transaction)
        return render(request, self.template, context=self.context)


class TransactionUpdate:
    '''Mixin for transaction update views'''
    form = None
    model = None
    context = None
    template = None

    def get(self, request, id):
        current_transaction = self.model.objects.get(id=id)
        bound_form = self.form(instance=current_transaction)
        self.context['form'] = bound_form
        return render(
            request, self.template, context=self.context)

    def post(self, request, id):
        current_transaction = self.model.objects.get(id=id)
        updated_bound_form = self.form(
            request.POST,
            instance=current_transaction)
        self.context['form'] = updated_bound_form
        if updated_bound_form.is_valid():
            updated_transaction = updated_bound_form.save()
            return redirect(updated_transaction)
        return render(
            request, self.template, context=self.context)


class TransactionDelete:
    '''Mixin for transaction delete views'''
    model = None
    template = None
    context = None
    success_url = None

    def get(self, request, id):
        current_transaction = self.model.objects.get(id=id)
        self.context['transaction'] = current_transaction
        return render(request, self.template, context=self.context)

    def post(self, request, id):
        current_transaction = self.model.objects.get(id=id)
        current_transaction.delete()
        return redirect(reverse(self.success_url))

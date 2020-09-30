from django import forms
from django.core.exceptions import ValidationError
from users.models import User
from .models import Transaction, InternalTransaction


class TransactionForm(forms.ModelForm):
    '''
    Form for creating and updating external transactions
    '''
    def clean_amount(self):
        '''
        Makes sure that the transaction amount is greater than 0
        '''
        new_amount = self.cleaned_data['amount']
        if new_amount <= 0:
            raise ValidationError('Сумма должна быть больше 0')
        return new_amount

    class Meta:
        model = Transaction
        fields = (
            'transaction_type', 'bank', 'amount', 'comment', 'date')

        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'rows': 3, 'cols': 20, 'class': 'form-control'}),

            'date': forms.DateInput(
                attrs={
                    'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'),

            'transaction_type': forms.Select(
                attrs={'class': 'form-control'}),

            'amount': forms.NumberInput(
                attrs={'class': 'form-control'}),

            'bank': forms.Select(
                attrs={'class': 'form-control'})
        }


class InternalTransactionForm(forms.ModelForm):
    '''
    Form for creating and updating internal transactions
    '''
    def clean_amount(self):
        '''
        Makes sure that the transaction amount is greater than 0
        '''
        new_amount = self.cleaned_data['amount']
        if new_amount <= 0:
            raise ValidationError('Сумма должна быть больше 0')
        return new_amount

    def clean_recipient_bank(self):
        '''
        Makes sure the transaction makes sense
        '''
        new_donor_bank = self.cleaned_data.get('donor_bank')
        new_donor_user = self.cleaned_data.get('donor_user')
        new_recipient_bank = self.cleaned_data.get('recipient_bank')
        new_recipient_user = self.cleaned_data.get('recipient_user')
        if (new_donor_bank == new_recipient_bank and
           new_donor_user == new_recipient_user):
            raise ValidationError('Бессмысленная операция:\
                перевод самому себе внутри одного банка')
        return new_recipient_bank

    class Meta:
        model = InternalTransaction
        exclude = ('author', 'creation_time', 'change_time')

        widgets = {
            'amount': forms.NumberInput(
                attrs={'class': 'form-control'}),

            'donor_user': forms.Select(
                attrs={'class': 'form-control'}),

            'donor_bank': forms.Select(
                attrs={'class': 'form-control'}),

            'recipient_user': forms.Select(
                attrs={'class': 'form-control'}),

            'recipient_bank': forms.Select(
                attrs={'class': 'form-control'}),

            'comment': forms.Textarea(
                attrs={
                    'rows': 3, 'cols': 20, 'class': 'form-control'}),

            'date': forms.DateInput(
                attrs={
                    'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'),
        }


class StatisticForm(forms.Form):
    '''
    Form for receiving data required for generating statistics
    '''
    user = forms.ModelChoiceField(
        label='Пользователь:',
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control mx-1'}))
    begin_date = forms.DateField(
        label='Начало периода:',
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control mx-1'},
            format='%Y-%m-%d'))
    end_date = forms.DateField(
        label='Конец периода:',
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control mx-1'},
            format='%Y-%m-%d'))

    def clean_end_date(self):
        current_end_date = self.cleaned_data['end_date']
        current_begin_date = self.cleaned_data['begin_date']
        if current_begin_date > current_end_date:
            raise ValidationError(
                'Конец периода не может быть раньше его начала')
        return current_end_date

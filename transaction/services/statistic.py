from transaction.models import TRANSACTION_TYPE_CHOICES
from django.db.models import Sum, F


class Statistic:
    def __init__(self, user, begin_date, end_date, *args, **kwargs):
        self.user = user
        self.date_range = [begin_date, end_date]

    def get_external_transactions_sums_by_types(self):
        '''
        Sends a query to the database to get summary values of external
        operations, grouped by their type
        '''
        queryset = (self.user.transactions
                    .filter(date__range=self.date_range)
                    .values('transaction_type')
                    .annotate(sum=Sum('amount')).order_by())
        int_key_output = {}
        for element in queryset:
            int_key_output[element['transaction_type']] = element['sum']
        output = {}
        for pair in TRANSACTION_TYPE_CHOICES:
            title = pair[1]
            amount = int_key_output.get(pair[0], 0)
            output[title] = amount
            if pair[0] == 1:
                output['В том числе налог'] = float(amount) * 0.06
                output['Итого, с учётом налога'] = float(amount) * 0.94
        return output

    def get_internal_transactions_sums_by_types(self):
        '''
        Sends a query to the database to get the total amount of money
        received from other users and the total amount of money
        transferred to other users.
        '''
        significant_operations = ((self.user.internal_write_offs.all() |
                                   self.user.internal_receipts.all())
                                  .filter(date__range=self.date_range)
                                  .exclude(donor_user=F('recipient_user')))
        significant_write_offs = significant_operations.filter(
            donor_user=self.user).aggregate(sum=Sum('amount'))
        significant_receipt = significant_operations.filter(
            recipient_user=self.user).aggregate(sum=Sum('amount'))
        return {
            'Переведено другим пользователям': (significant_write_offs['sum']
                                                or 0),
            'Получено от других пользователей': (significant_receipt['sum']
                                                 or 0)}

    def get_card_withdrawals_by_banks(self):
        '''
        Sends a query to the database to get the total withdrawal amount
        through each bank
        '''
        return (self.user.transactions
                .filter(date__range=self.date_range)
                .filter(transaction_type=3)
                .values('bank')
                .annotate(sum=Sum('amount')))

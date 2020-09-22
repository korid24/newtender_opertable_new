from django.db.models import Q, F, Sum
from django.utils import timezone
from .models import Transaction, InternalTransaction
from users.models import User


def statistic(user_id, month=timezone.now().month):
    print(month)
    print(user_id)
    return [User.objects.values('transactions__transaction_type')
            .annotate(total_amount=Sum('transactions__amount'))
            .filter(id=user_id)
            .filter(transactions__date__month=month)]

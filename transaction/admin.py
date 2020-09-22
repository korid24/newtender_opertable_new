from django.contrib import admin
from .models import Transaction, InternalTransaction

admin.site.register(Transaction)
admin.site.register(InternalTransaction)

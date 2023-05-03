from django.contrib import admin

from .models import Transaction, TransactionDetail

admin.site.register(Transaction)
admin.site.register(TransactionDetail)

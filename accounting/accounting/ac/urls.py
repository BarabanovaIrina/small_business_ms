from django.urls import path

from .views import TransactionDetail, TransactionsView

urlpatterns = [
    path("transactions", TransactionsView.as_view()),
    path("transactions/<int:pk>", TransactionDetail.as_view()),
]

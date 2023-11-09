from django.urls import path
from .views import UserListView, ExpenseListView,BalanceListView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('expenses/', ExpenseListView.as_view(), name='expense-list'),
    path('balances/', BalanceListView.as_view(), name='balance-list'),
]

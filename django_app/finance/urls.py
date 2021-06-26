from django.urls import path, include

from .views import (
    TransactionCategoryDebitCreateView,
    TransactionCategoryCreditCreateView,
    TransactionDebitCreateView,
    TransactionCreditCreateView,
    TransactionDebitUpdateView,
    TransactionCreditUpdateView,
    FilteredTransactionTableView,
    TransactionDeleteView,
    HomeView
)


app_name = 'finance'

transaction_category_urlpatterns = ([
    path('create/', include(([
        path('debit/',
             TransactionCategoryDebitCreateView.as_view(),
             name='debit'),
        path('credit/',
             TransactionCategoryCreditCreateView.as_view(),
             name='credit')
    ], 'create'), namespace=None)),
], 'transaction_category')

transaction_urlpatterns = ([
    path('create/', include(([
        path('debit/',
             TransactionDebitCreateView.as_view(),
             name='debit'),
        path('credit/',
             TransactionCreditCreateView.as_view(),
             name='credit')
    ], 'create'), namespace=None)),
    path('update/', include(([
        path('debit/<int:pk>/',
             TransactionDebitUpdateView.as_view(),
             name='debit'),
        path('credit/<int:pk>/',
             TransactionCreditUpdateView.as_view(),
             name='credit')
    ], 'update'), namespace=None)),
    path('table/', FilteredTransactionTableView.as_view(), name='table'),
    path('main/', HomeView.as_view(), name='main'),
    path('delete/<int:pk>/', TransactionDeleteView.as_view(), name='delete'),
], 'transaction')


urlpatterns = [
    path('transaction_category/', include(transaction_category_urlpatterns)),
    path('transaction/', include(transaction_urlpatterns)),
]

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
    HomeView,
    PeriodicTransactionCreditCreateView,
    PeriodicTransactionCreditUpdateView,
    PeriodicTransactionDeleteView,
    TransactionFromPeriodicCreditCreateView,
    FilteredPeriodicTransactionTableView
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
             name='credit'),
        path('credit/from/periodic/<int:pk>/',
             TransactionFromPeriodicCreditCreateView.as_view(),
             name='credit_from_periodic')
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
    # path('main/', HomeView.as_view(), name='main'),
    path('delete/<int:pk>/', TransactionDeleteView.as_view(), name='delete'),
], 'transaction')

periodic_transaction_urlpatterns = ([
    path('create/', include(([
        path('credit/',
             PeriodicTransactionCreditCreateView.as_view(),
             name='credit')
    ], 'create'), namespace=None)),
    path('update/', include(([
        path('credit/<int:pk>/',
             PeriodicTransactionCreditUpdateView.as_view(),
             name='credit')
    ], 'update'), namespace=None)),
    path('table/', FilteredPeriodicTransactionTableView.as_view(), name='table'),
    path('delete/<int:pk>/', PeriodicTransactionDeleteView.as_view(), name='delete'),
], 'periodic_transaction')


urlpatterns = [
    path('main/', HomeView.as_view(), name='main'),
    path('transaction_category/', include(transaction_category_urlpatterns)),
    path('transaction/', include(transaction_urlpatterns)),
    path('periodic_transaction/', include(periodic_transaction_urlpatterns)),
]

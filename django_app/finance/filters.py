import django_filters

from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    datetime = django_filters.DateRangeFilter()

    class Meta:
        model = Transaction
        fields = ('datetime', 'currency', 'category', 'user')


class TransactionDateFilter(django_filters.FilterSet):
    datetime = django_filters.DateRangeFilter()

    class Meta:
        model = Transaction
        fields = ('datetime',)

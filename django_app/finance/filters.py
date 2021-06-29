import django_filters

from .models import Transaction, PeriodicTransaction, TransactionCategory


class TransactionFilter(django_filters.FilterSet):
    """
    Фильтр для транзакций
    """
    datetime = django_filters.DateRangeFilter()

    class Meta:
        model = Transaction
        fields = ('datetime', 'currency', 'category', 'user')


class TransactionDateFilter(django_filters.FilterSet):
    """
    Фильтр только по дате для главной страницы
    """
    datetime = django_filters.DateRangeFilter()

    class Meta:
        model = Transaction
        fields = ('datetime',)


class PeriodicTransactionFilter(django_filters.FilterSet):
    """
    Фильтр для периодических транзакций
    """

    class Meta:
        model = PeriodicTransaction
        fields = ('currency', 'category', 'user')


class TransactionCategoryFilter(django_filters.FilterSet):
    """
    Фильтр для категорий транзакций
    """
    transactions__datetime = django_filters.DateRangeFilter()

    class Meta:
        model = TransactionCategory
        fields = ('transactions__datetime', 'transactions__user')

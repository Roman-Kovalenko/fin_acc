from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

import django_tables2 as tables

from .utils import build_link
from .models import Transaction, PeriodicTransaction


class TransactionTable(tables.Table):
    """
    Таблица транзакций
    """
    get_action = tables.Column(
        verbose_name=_('actions'), orderable=False, accessor='pk')

    def render_get_action(self, record):
        return mark_safe(
            '<br>'.join((
                build_link(record.get_update_url(), text='Редактировать'),
                build_link(
                    '#',
                    text='Удалить',
                    attrs={
                        'data-bs-toggle': 'modal',
                        'data-bs-target': '#deleteDialogModal',
                        'data-bs-del-url': record.get_delete_url()
                    }
                )
            ))
        )

    class Meta:
        model = Transaction
        sequence = ('datetime', 'amount', 'currency',
                    'category', 'user', 'comment', 'receipt', 'get_action')
        exclude = ('id', 'periodic_transaction')
        row_attrs = {
            'class': lambda record: 'table-success' if record.category.is_debit else 'table-danger'
        }


class PeriodicTransactionTable(tables.Table):
    """
    Таблица периодических транзакций
    """
    get_action = tables.Column(
        verbose_name=_('actions'), orderable=False, accessor='pk')

    def render_get_action(self, record):
        return mark_safe(
            '<br>'.join((
                build_link(record.get_update_url(), text='Редактировать'),
                build_link(
                    '#',
                    text='Удалить',
                    attrs={
                        'data-bs-toggle': 'modal',
                        'data-bs-target': '#deleteDialogModal',
                        'data-bs-del-url': record.get_delete_url()
                    }
                )
            ))
        )

    class Meta:
        model = PeriodicTransaction
        sequence = ('name', 'start_date', 'end_date', 'pay_day',
                    'amount', 'currency', 'category', 'user', 'comment')
        exclude = ('id',)
        row_attrs = {
            'class': lambda record: 'table-success' if record.category.is_debit else 'table-danger'
        }


class CurrentMonthPeriodicTransactionTable(tables.Table):
    """
    Таблица периодических транзакций за текущий месяц
    """
    amount_sum = tables.Column(verbose_name=_('paid'), empty_values=())
    need_pay = tables.Column(verbose_name=_('unpaid'), empty_values=())

    get_action = tables.Column(
        verbose_name=_('actions'), orderable=False, accessor='pk')

    def render_get_action(self, record):
        return build_link(record.get_create_transaction_from_periodic_url(), text='Оплатить')

    class Meta:
        model = PeriodicTransaction
        sequence = ('name', 'amount', 'amount_sum',
                    'need_pay', 'pay_day', 'get_action')
        exclude = ('id', 'currency', 'category', 'user',
                   'comment', 'start_date', 'end_date',)
        row_attrs = {
            'class': lambda record: 'table-danger' if record.need_pay > 0 else 'table-success'
        }

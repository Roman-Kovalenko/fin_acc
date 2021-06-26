from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

import django_tables2 as tables

from .utils import build_link
from .models import Transaction


class TransactionTable(tables.Table):
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
        template_name = 'django_tables2/bootstrap.html'
        sequence = ('datetime', 'amount', 'currency',
                    'category', 'user', 'comment', 'receipt', 'get_action')
        exclude = ('id', )
        row_attrs = {
            'class': lambda record: 'table-success' if record.category.is_debit else 'table-danger'
        }

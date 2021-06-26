from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


User = get_user_model()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<datetime>/<filename>
    return f'user_{instance.user.id}/{instance.datetime:%Y-%m-%d_%H-%M-%S}/{filename}'


def get_ruble_currency():
    currency, _ = Currency.objects.get_or_create(name='Рубль')
    return currency


class Currency(models.Model):
    """
    Модель валюты
    """
    name = models.CharField(_('name'), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'currency'
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')


class TransactionCategory(models.Model):
    """
    Модель категории транзакий
    """
    name = models.CharField(_('name'), max_length=100, unique=True)
    is_debit = models.BooleanField(_('is debit'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'transaction_category'
        verbose_name = _('transaction category')
        verbose_name_plural = _('transaction categories')


class Transaction(models.Model):
    """
    Модель транзакций
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='transactions'
    )
    category = models.ForeignKey(
        TransactionCategory,
        on_delete=models.CASCADE,
        verbose_name=_('category'),
        related_name='transactions'
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        default=get_ruble_currency,
        verbose_name=_('currency'),
        related_name='transactions'
    )

    amount = models.DecimalField(_('amount'), max_digits=50, decimal_places=2)
    datetime = models.DateTimeField(_('date and time'), default=datetime.now)
    comment = models.TextField(_('comment'), blank=True)
    receipt = models.ImageField(
        _('receipt'),
        upload_to=user_directory_path,
        blank=True,
        default=None,
    )

    def get_update_url(self) -> str:
        type_str = 'debit' if self.category.is_debit else 'credit'
        return reverse(f'finance:transaction:update:{type_str}',
                       kwargs={'pk': self.id})

    def get_delete_url(self) -> str:
        return reverse('finance:transaction:delete', kwargs={'pk': self.id})

    def __str__(self):
        return f'{self.amount} {self.datetime} {self.user}'

    class Meta:
        ordering = ['datetime']
        db_table = 'transaction'
        verbose_name = _('transaction')
        verbose_name_plural = _('transactios')

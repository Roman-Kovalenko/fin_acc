from datetime import datetime, date

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .managers import PeriodicTransactionQuerySet


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


# TODO: Добавить миграции с заготовленными категориями транзакций
class TransactionCategory(models.Model):
    """
    Модель категории транзакций
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


class PeriodicTransaction(models.Model):
    """
    Модель для повторяющихся ежемесячных транзакций
    """
    objects = PeriodicTransactionQuerySet.as_manager()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='periodic_transactions'
    )
    category = models.ForeignKey(
        TransactionCategory,
        on_delete=models.CASCADE,
        verbose_name=_('category'),
        related_name='periodic_transactions'
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        default=get_ruble_currency,
        verbose_name=_('currency'),
        related_name='periodic_transactions'
    )

    name = models.CharField(_('name'), max_length=100, unique=True)
    start_date = models.DateField(_('start date'), default=date.today)
    end_date = models.DateField(
        _('end date'),
        null=True,
        blank=True,
        default=None
    )
    # TODO: Подумать над логикой для месяцев где не 31 день
    pay_day = models.PositiveSmallIntegerField(
        _('pay day'),
        validators=(
            MinValueValidator(1),
            MaxValueValidator(31),
        )
    )
    amount = models.DecimalField(_('amount'), max_digits=50, decimal_places=2)
    comment = models.TextField(_('comment'), blank=True)

    def __str__(self):
        return f'{self.name}. {self.amount} каждое {self.pay_day} число месяца'

    def get_update_url(self) -> str:
        type_str = 'debit' if self.category.is_debit else 'credit'
        return reverse(f'finance:periodic_transaction:update:{type_str}',
                       kwargs={'pk': self.id})

    def get_delete_url(self) -> str:
        return reverse('finance:periodic_transaction:delete', kwargs={'pk': self.id})

    def get_create_transaction_from_periodic_url(self) -> str:
        type_str = 'debit' if self.category.is_debit else 'credit'
        return reverse(f'finance:transaction:create:{type_str}_from_periodic',
                       kwargs={'pk': self.id})

    class Meta:
        ordering = ['pay_day']
        db_table = 'periodic_transaction'
        verbose_name = _('periodic transaction')
        verbose_name_plural = _('periodic transactions')


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
    periodic_transaction = models.ForeignKey(
        PeriodicTransaction,
        on_delete=models.SET_NULL,
        verbose_name=_('periodic transaction'),
        null=True,
        blank=True,
        default=None
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.periodic_transaction:
            self.category = self.periodic_transaction.category

    class Meta:
        ordering = ['datetime']
        db_table = 'transaction'
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')

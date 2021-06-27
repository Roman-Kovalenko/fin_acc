from datetime import date

from django.db.models import F, Q, QuerySet, Sum, DecimalField, ExpressionWrapper
from django.db.models.functions import Coalesce

from .utils import get_current_month_date_range


class PeriodicTransactionQuerySet(QuerySet):
    """
    QuerySet для ежемесячных транзакций
    """

    def actual_in_current_month(self):
        """
        Возвращает только актуальные в текущем месяце периодические транзакции
        """
        start_period, end_period = get_current_month_date_range()
        return self.filter(
            Q(end_date__isnull=True) | Q(end_date__gte=end_period)
        ).filter(start_date__lte=start_period)

    def with_amount_sum_between_dates(
            self, start_period: date, end_period: date):
        """
        Возвращает сумму amount по периодическим транзакциям за период
        """
        return self.annotate(
            amount_sum=Coalesce(
                Sum(
                    'transaction__amount',
                    filter=Q(transaction__datetime__date__range=(
                        start_period,
                        end_period
                    ))
                ),
                0,
                output_field=DecimalField(decimal_places=2)
            ),
            need_pay=ExpressionWrapper(
                F('amount_sum') - F('amount'),
                output_field=DecimalField(decimal_places=2)
            )
        )

    def with_amount_sum_in_current_month(self):
        """
        Возвращает сумму amount по периодическим транзакциям за текущий месяц
        """
        month_date_range = get_current_month_date_range()
        return self.with_amount_sum_between_dates(*month_date_range)

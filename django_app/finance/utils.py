import calendar
from datetime import date
from urllib.parse import urlencode
from typing import Optional, Tuple

from django.utils.html import escape
from django.utils.safestring import mark_safe

from django_tables2.utils import AttributeDict


def build_link(url: str, get: Optional[dict] = None, text: Optional[str] = None,
               attrs: Optional[dict] = None, as_is: bool = False) -> str:
    """
    Возвращает экранированный html тег a для использования в шаблонах django
    """
    if get:
        url = '?'.join([url, urlencode(get)])
    if not text:
        text = url
    elif text and not as_is:
        text = escape(text)
    attrs = AttributeDict(attrs if attrs else {})
    attrs['href'] = url
    html = f'<a {attrs.as_html()}>{text}</a>'
    return mark_safe(html)


def get_current_month_date_range() -> Tuple[date, date]:
    """
    Возвращает начальную и конечную дату текущего месяца
    """
    first_date_of_current_month = date.today().replace(day=1)
    _, last_day = calendar.monthrange(
        first_date_of_current_month.year,
        first_date_of_current_month.month
    )
    last_date_of_current_month = first_date_of_current_month.replace(
        day=last_day
    )
    return (first_date_of_current_month, last_date_of_current_month)

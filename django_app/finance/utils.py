from urllib.parse import urlencode
from typing import Optional

from django.utils.html import escape
from django.utils.safestring import mark_safe

from django_tables2.utils import AttributeDict


def build_link(url: str, get: Optional[dict] = None, text: Optional = None,
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

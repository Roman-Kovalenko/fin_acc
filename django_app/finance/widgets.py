from django.forms import Select


# TODO: Сделать более универсальное решение
# В текущей реализации ждет, что в основном шаблоне будет модалка и js
class SelectWithCreateButton(Select):
    """
    Виджет, добавляющий к стандартному селекту кнопку по которой будем
    открывать модалку с возможностью создания объекта
    """
    template_name = 'finance/widgets/select_with_create_button.html'

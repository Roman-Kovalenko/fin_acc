from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .models import TransactionCategory, Transaction
from .forms import TransactionCategoryForm, TransactionForm
from .filters import TransactionFilter
from .tables import TransactionTable


class TransactionCategoryCreateMixin():
    """
    Mixin создания категории транзакции
    """
    model = TransactionCategory
    success_url = reverse_lazy('home')
    form_class = TransactionCategoryForm
    success_message = _('Transaction category was created successfully')


@method_decorator(login_required, name='dispatch')
class TransactionCategoryDebitCreateView(
        TransactionCategoryCreateMixin, SuccessMessageMixin, CreateView):
    """
    View создания категории транзакции с is_debit = True
    """
    initial = {'is_debit': True}
    extra_context = {'title': _('Create debit transaction category')}


@method_decorator(login_required, name='dispatch')
class TransactionCategoryCreditCreateView(
        TransactionCategoryCreateMixin, SuccessMessageMixin, CreateView):
    """
    View создания категории транзакции с is_debit = False
    """
    initial = {'is_debit': False}
    extra_context = {'title': _('Create credit transaction category')}


class TransactionMixin():
    """
    базовый Mixin транзакции
    """
    model = Transaction
    success_url = reverse_lazy('home')
    form_class = TransactionForm


class TransactionCreateMixin(TransactionMixin):
    """
    Mixin создания транзакции
    """

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class TransactionDebitCreateView(
        TransactionCreateMixin, SuccessMessageMixin, CreateView):
    """
    View создания транзакций с is_debit = True
    """
    initial = {'is_debit': True}
    extra_context = {'title': _('Create debit transaction')}
    success_message = _('Transaction debit was created successfully')


@method_decorator(login_required, name='dispatch')
class TransactionCreditCreateView(
        TransactionCreateMixin, SuccessMessageMixin, CreateView):
    """
    View создания транзакций с is_debit = False
    """
    initial = {'is_debit': False}
    extra_context = {'title': _('Create credit transaction')}
    success_message = _('Transaction credit was created successfully')


@method_decorator(login_required, name='dispatch')
class TransactionDebitUpdateView(
        TransactionMixin, SuccessMessageMixin, UpdateView):
    """
    View редактирования транзакций с is_debit = True
    """
    initial = {'is_debit': True}
    extra_context = {'title': _('Update debit transaction')}
    success_message = _('Transaction debit was updated successfully')


@method_decorator(login_required, name='dispatch')
class TransactionCreditUpdateView(
        TransactionMixin, SuccessMessageMixin, UpdateView):
    """
    View редактирования транзакций с is_debit = False
    """
    initial = {'is_debit': False}
    extra_context = {'title': _('Update credit transaction')}
    success_message = _('Transaction credit was updated successfully')


@method_decorator(login_required, name='dispatch')
class TransactionDeleteView(TransactionMixin, SuccessMessageMixin, DeleteView):
    """
    View удаления транзакций с is_debit = True
    """
    success_message = _('Transaction was deleted')


@method_decorator(login_required, name='dispatch')
class FilteredTransactionTableView(SingleTableMixin, FilterView):
    table_class = TransactionTable
    model = Transaction
    template_name = 'finance/filtered_table.html'
    filterset_class = TransactionFilter
    extra_context = {'title': _('Transaction table with filter')}

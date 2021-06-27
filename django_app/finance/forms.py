from django import forms
from django.utils.translation import gettext_lazy as _

from .models import TransactionCategory, Transaction, PeriodicTransaction


class TransactionCategoryForm(forms.ModelForm):
    """
    Форма категорий транзакций
    """
    class Meta:
        model = TransactionCategory
        fields = ('name', 'is_debit')
        widgets = {'is_debit': forms.HiddenInput}


# TODO: Добавить рядом с выбором категорий кнопку, открывающую модальное окно
# с формой создания категории
class TransactionForm(forms.ModelForm):
    """
    Форма создания транзакции
    """
    class Meta:
        model = Transaction
        fields = ('datetime', 'amount', 'currency', 'category',
                  'periodic_transaction', 'comment', 'receipt')
        widgets = {'periodic_transaction': forms.HiddenInput}

    def __init__(self, *args, **kwargs):
        self.is_debit = kwargs['initial'].pop('is_debit')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = TransactionCategory.objects.filter(
            is_debit=self.is_debit)
        self.fields['periodic_transaction'].queryset = (
            PeriodicTransaction.objects.filter(
                category__is_debit=self.is_debit)
        )
        if self.is_debit:
            number_attrs = {'min': 0.01, 'step': 0.01}
        else:
            number_attrs = {'max': -0.01, 'step': 0.01}
        self.fields['amount'].widget = forms.NumberInput(attrs=number_attrs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if self.is_debit and amount <= 0:
            raise forms.ValidationError(_('Only positive allowed'))
        elif not self.is_debit and amount >= 0:
            raise forms.ValidationError(_('Only negative allowed'))
        return amount


class PeriodicTransactionForm(forms.ModelForm):
    """
    Форма периодических транзакций
    """
    class Meta:
        model = PeriodicTransaction
        fields = ('name', 'category', 'amount', 'currency',
                  'start_date', 'end_date', 'pay_day', 'comment')
        widgets = {'pay_day': forms.NumberInput(attrs={'min': 1, 'max': 31})}

    def __init__(self, *args, **kwargs):
        self.is_debit = kwargs['initial'].pop('is_debit')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = TransactionCategory.objects.filter(
            is_debit=self.is_debit)
        if self.is_debit:
            number_attrs = {'min': 0.01, 'step': 0.01}
        else:
            number_attrs = {'max': -0.01, 'step': 0.01}
        self.fields['amount'].widget = forms.NumberInput(attrs=number_attrs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if self.is_debit and amount <= 0:
            raise forms.ValidationError(_('Only positive allowed'))
        elif not self.is_debit and amount >= 0:
            raise forms.ValidationError(_('Only negative allowed'))
        return amount


class TransactionFromPeriodicTransactionForm(forms.ModelForm):
    """
    Форма создания транзакции из периодической транзакции
    """
    class Meta:
        model = Transaction
        fields = ('datetime', 'amount', 'currency', 'category',
                  'periodic_transaction', 'comment', 'receipt')
        widgets = {'category': forms.HiddenInput}

    def __init__(self, *args, **kwargs):
        self.is_debit = kwargs['initial'].pop('is_debit')
        super().__init__(*args, **kwargs)
        self.fields['periodic_transaction'].queryset = (
            PeriodicTransaction.objects.filter(
                category__is_debit=self.is_debit)
        )
        if self.is_debit:
            number_attrs = {'min': 0.01, 'step': 0.01}
            self.fields['periodic_transaction'].widget = forms.HiddenInput()
        else:
            number_attrs = {'max': -0.01, 'step': 0.01}
        self.fields['amount'].widget = forms.NumberInput(attrs=number_attrs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if self.is_debit and amount <= 0:
            raise forms.ValidationError(_('Only positive allowed'))
        elif not self.is_debit and amount >= 0:
            raise forms.ValidationError(_('Only negative allowed'))
        return amount

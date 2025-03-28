from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'description', 'amount', 'transaction_type']

class FinancialStatementForm(forms.Form):
    statement_date = forms.DateField()
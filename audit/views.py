from django.shortcuts import render, redirect

from rest_framework import viewsets
from .models import Transaction, FinancialStatement
from .serializers import TransactionSerializer, FinancialStatementSerializer
from .forms import TransactionForm, FinancialStatementForm
from django.db.models import Sum

# Create your views here.

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class FinancialStatementViewSet(viewsets.ModelViewSet):
    queryset = FinancialStatement.objects.all()
    serializer_class = FinancialStatementSerializer

def home(request):
    return render(request, 'audit/home.html')

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_transactions')
    else:
        form = TransactionForm()
    return render(request, 'audit/add_transactions.html', {'form': form})

def view_transactions(request):
    transactions = Transaction.objects.all()
    return render(request, 'audit/view_transactions.html', {'transactions': transactions})

def generate_statement(request):
    if request.method == 'POST':
        form = FinancialStatementForm(request.POST)
        if form.is_valid():
            statement_date = form.cleaned_data['statement_date']
            total_income = Transaction.objects.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
            total_expense = Transaction.objects.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
            net_income = total_income - total_expense
            statement = FinancialStatement.objects.create(statement_date=statement_date, total_income=total_income, total_expense=total_expense, net_income=net_income)
            return render(request, 'audit/generate_statements.html', {'form': form, 'statement': statement})
    else:
        form = FinancialStatementForm()
    return render(request, 'audit/generate_statements.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404

from rest_framework import viewsets
from .models import Transaction, FinancialStatement
from .serializers import TransactionSerializer, FinancialStatementSerializer
from .forms import TransactionForm, FinancialStatementForm
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import render_to_string
# from xhtml2pdf import pisa
# from .models import FinancialStatement

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

# def generate_pdf(html):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="financial_statement.pdf"'
#     pisa_status = pisa.CreatePDF(html, dest=response)
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response

# def download_statement(request, statement_id):
#     statement = FinancialStatement.objects.get(id=statement_id)
#     html = render_to_string('audit/statement_pdf.html', {'statement': statement})
#     return generate_pdf(html)

def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        transaction.delete()
        return redirect('view_transactions')
    return render(request, 'audit/view_transactions.html', {'transactions': Transaction.objects.all()})

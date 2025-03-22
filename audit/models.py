from django.db import models

# Create your models here.

class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50)  # e.g., income, expense

    def __str__(self):
        return f"{self.date} - {self.description} - {self.amount}"

class FinancialStatement(models.Model):
    statement_date = models.DateField()
    total_income = models.DecimalField(max_digits=10, decimal_places=2)
    total_expense = models.DecimalField(max_digits=10, decimal_places=2)
    net_income = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Statement for {self.statement_date}"



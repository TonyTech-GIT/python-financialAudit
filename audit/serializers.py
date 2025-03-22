from rest_framework import serializers
from .models import Transaction, FinancialStatement

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class FinancialStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialStatement
        fields = '__all__'
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-transactions/', views.add_transaction, name='add_transactions'),
    path('view-transactions/', views.view_transactions, name='view_transactions'),
    path('generate-statements/', views.generate_statement, name='generate_statements'),
    # path('download-statement/<int:statement_id>/', views.download_statement, name='download_statement'),
    path('delete-transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
]
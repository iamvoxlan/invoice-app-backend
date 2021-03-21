from django.urls import path
from invoice.views import *
# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('invoice/', InvoiceListView.as_view(), name="invoice"),
    path('invoice/<int:pk>', InvoiceDetailView.as_view(), name="invoice-detail"),
    path('customer/', CustomerListView.as_view(), name="customer"),
    path('last-transaction/', LastTransactionListView.as_view(), name="last-transaction"),
]

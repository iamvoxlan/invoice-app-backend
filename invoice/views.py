from rest_framework import status
from backend.helper.response import Response
from django.contrib import auth
from rest_framework.generics import GenericAPIView
from invoice.serializers import *
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db import transaction

# Create your views here.

class InvoiceListView(GenericAPIView):
    serializers_class = InvoiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = InvoiceListSerializer(invoices, many=True)

        if not request.user.is_authenticated:
            return Response.badRequest(
                data=None,
                message="Not authenticated",
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response.ok(
            data=serializer.data,
            message="Invoice list",
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if not request.user.is_authenticated:
            return Response.badRequest(
                data=None,
                message="Not authenticated",
                status=status.HTTP_403_FORBIDDEN,
            )
        if not request.user.role == 'S':
            return Response.badRequest(
                data=None,
                message="Current user not permitted",
                status=status.HTTP_403_FORBIDDEN,
            )
        if serializer.is_valid():
            data = serializer.data
            
            invoice_number = data['number']
            invoice_date = data['date']
            customer_id = data['customer_id']
            with transaction.atomic():

                invoice = Invoice(number=invoice_number, date=invoice_date, customer_id=Customer.objects.get(id=customer_id))
                invoice.save()

                invoice_id = invoice.id

                item_list = data['item_list']

                ordered_item_instance = [
                    OrderedItem(
                        name = single_item['name'],
                        qty = single_item['qty'],
                        price = single_item['price'],
                        invoice_id = Invoice.objects.get(id=invoice_id)
                    ) for single_item in item_list
                ]
            
                OrderedItem.objects.bulk_create(ordered_item_instance)

            return Response.ok(
                data = invoice_id,
                status = status.HTTP_200_OK,
                message= "Add invoice succeed"
            )
        return Response.badRequest(
            data=serializer.errors,
            message="Add invoice failed",
            status=status.HTTP_400_BAD_REQUEST,
        )

class InvoiceDetailView(GenericAPIView):
    serializers_class = InvoiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response.badRequest(
                data=None,
                message="Not authenticated",
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            invoice = Invoice.objects.get(id=pk)
        except Invoice.DoesNotExist:
            invoice = None
        
        if invoice is None:
            return Response.badRequest(
                data=None,
                message="Invoice not found",
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = InvoiceListSerializer(invoice)

        data = serializer.data

        try:
            ordered_item = OrderedItem.objects.filter(invoice_id=data['id'])
        except OrderedItem.DoesNotExist:
            ordered_item = None

        item_serializer = OrderedItemListSerializer(ordered_item, many=True)

        data.update({'ordered_item': item_serializer.data})

        return Response.ok(
            data=data,
            message="Invoice detail",
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        serializer = InvoiceSerializer(data=request.data)
        if not request.user.is_authenticated:
            return Response.badRequest(
                data=None,
                message="Not authenticated",
                status=status.HTTP_403_FORBIDDEN,
            )
        if not request.user.role == 'S' or request.user.role == 'L':
            return Response.badRequest(
                data=None,
                message="Current user not permitted",
                status=status.HTTP_403_FORBIDDEN,
            )
        if serializer.is_valid():
            data = serializer.data
            invoice_number = data['number']
            invoice_date = data['date']
            customer_id = data['customer_id']
            item_list = data['item_list']

            #update data
            with transaction.atomic():

                OrderedItem.objects.filter(invoice_id=pk).delete()

                Invoice.objects.filter(id=pk).update(
                    number = invoice_number,
                    date = invoice_date,
                    customer_id = customer_id
                )
                ordered_item_instance = [
                    OrderedItem(
                        name = single_item['name'],
                        qty = single_item['qty'],
                        price = single_item['price'],
                        invoice_id = Invoice.objects.get(id=pk)
                    ) for single_item in item_list
                ]
            
                OrderedItem.objects.bulk_create(ordered_item_instance)

            return Response.ok(
                data = None,
                status = status.HTTP_200_OK,
                message= "Edit invoice succeed"
            )
        return Response.badRequest(
            data=serializer.errors,
            message="Edit invoice failed",
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response.badRequest(
                data=None,
                message="Not authenticated",
                status=status.HTTP_403_FORBIDDEN,
            )
        if not request.user.role == 'L':
            return Response.badRequest(
                data=None,
                message="Current user not permitted",
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            invoice = Invoice.objects.get(id=pk)
        except Invoice.DoesNotExist:
            invoice = None

        if invoice is None:
            return Response.badRequest(
                data=None,
                message="Not fouond",
                status=status.HTTP_404_NOT_FOUND,
            )
        
        invoice.delete()
        return Response.ok(
            data=None,
            message="Invoice deleted",
            status=status.HTTP_200_OK
        )
        
        
class CustomerListView(GenericAPIView):
    serializers_class = CustomerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        cutomers = Customer.objects.all()
        serializer = CustomerSerializer(cutomers, many=True)

        if not request.user.is_authenticated:
            return Response.badRequest(
                data=None,
                message="Not authenticated",
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response.ok(
            data=serializer.data,
            message="Customer list",
            status=status.HTTP_200_OK,
        )

    def post(self, request):
            
        if not request.user.is_authenticated:
            return Response.badRequest(
                data=None,
                message="Not authenticated",
                status=status.HTTP_403_FORBIDDEN,
            )
        if not request.user.role == 'S':
            return Response.badRequest(
                data=None,
                message="Current user not permitted",
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response.ok(
                data = serializer.data,
                status = status.HTTP_200_OK,
                message= "Add customer succeed"
            )
        return Response.badRequest(
            data=serializer.errors,
            message="Add customer failed",
            status=status.HTTP_400_BAD_REQUEST,
        )

class LastTransactionListView(GenericAPIView):
    serializers_class = InvoiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        invoices = Invoice.objects.order_by('-id').distinct('customer_id')
        serializer = InvoiceListSerializer(invoices, many=True)

        if not request.user.is_authenticated:
            return Response.badRequest(
                data=None,
                message="Not authenticated",
                status=status.HTTP_403_FORBIDDEN,
            )

        if not request.user.role == 'D':
            return Response.badRequest(
                data=None,
                message="Current role not  permitted",
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response.ok(
            data=serializer.data,
            message="Invoice list",
            status=status.HTTP_200_OK,
        )
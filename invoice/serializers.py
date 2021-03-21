from invoice.models import *
from rest_framework import serializers
from django.db.models import Sum, F, FloatField
class InputOrderedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedItem
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    item_list = serializers.ListField(child=InputOrderedItemSerializer())
    class Meta:
        model = Invoice
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        
class InvoiceListSerializer(serializers.ModelSerializer):
    customer_id = serializers.SerializerMethodField()
    invoice_amount = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = '__all__'

    def get_customer_id(self, obj):
        customer_id = obj.customer_id
        if customer_id is not None:
            customer_id = CustomerSerializer(customer_id).data
        return customer_id

    def get_invoice_amount(self, obj):
        invoice_id = obj.id
        # invoice_amount = OrderedItem.objects.filter(invoice_id=invoice_id).aggregate(
        #     total = Sum('price', field='price * qty')
        # )['total']
        invoice_amount = OrderedItem.objects.filter(invoice_id=invoice_id).aggregate(sum=Sum(F('price')*F('qty'), output_field=FloatField()))["sum"]
        if invoice_amount is None:
            return 0
        return invoice_amount * 1.1


class OrderedItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedItem
        fields = '__all__'
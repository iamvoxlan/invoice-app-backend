from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    class Meta:
        db_table = 'customer'

class Invoice(models.Model):
    number = models.CharField(max_length=255)
    date = models.DateField()
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        db_table = 'invoice'

class OrderedItem(models.Model):
    name = models.CharField(max_length=255)
    qty = models.IntegerField()
    price = models.FloatField()
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'ordered_item'
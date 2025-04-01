from django.db import models
import uuid
# Create your models here.

class MpesaTransaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    merchant_request_id = models.CharField(max_length=255, unique=True)
    checkout_request_id = models.CharField(max_length=255, unique=True)
    result_code = models.IntegerField()
    result_desc = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mpesa_receipt_number = models.CharField(max_length=255, null=True, blank=True, unique=True)
    transaction_date = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Transaction {self.mpesa_receipt_number} - {self.amount}"
    
class Subscription(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    
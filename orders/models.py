from django.db import models
from acounts.models import Account
from store.models import Product, Variation

class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length = 100)
    payment_method = models.CharField(max_length = 100)
    amount_paid = models.CharField(max_length =100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.payment_id



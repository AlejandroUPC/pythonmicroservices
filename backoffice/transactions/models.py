from django.db import models
from .utils import create_random_id


class Customer(models.Model):
    customer_id = models.BigIntegerField(
        default=create_random_id(), null=False, primary_key=True)
    register_date = models.DateField(auto_now=True)
    previous_ctmer = models.BooleanField(default=False)
    has_sons = models.BooleanField()
    is_married = models.BooleanField()
    is_local = models.BooleanField()
    residence = models.CharField(max_length=50)
    address = models.CharField(max_length=50)


class SuperMarket(models.Model):
    supermarket_id = models.BigIntegerField(
        default=create_random_id(), null=False, primary_key=True)
    supermarket_name = models.CharField(max_length=100)
    register_date = models.DateField(auto_now=True)


class Transaction(models.Model):
    customer_id = models.ForeignKey(
        to=Customer, to_field="customer_id", on_delete=models.CASCADE)
    transaction_id = models.BigIntegerField(primary_key=True,
                                            null=False, default=create_random_id())
    item_id = models.BigIntegerField()
    pay_method = models.IntegerField()
    price = models.FloatField()
    item_cnt = models.SmallIntegerField()
    bill_id = models.BigIntegerField()
    sp_owner = models.ForeignKey(
        to=SuperMarket, to_field="supermarket_id", on_delete=models.CASCADE)
    transaction_dt = models.DateField(auto_now=True)

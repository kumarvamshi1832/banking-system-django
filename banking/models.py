from django.db import models

# Create your models here.
class Bank(models.Model):
    cid=models.IntegerField(primary_key=True)
    cname=models.CharField(max_length=30)
    accountnumber=models.IntegerField()
    email=models.EmailField(unique=True)
    phoneno=models.CharField(max_length=10)
    password=models.CharField(max_length=20)
    address=models.TextField()
    dob=models.DateField()
    balance = models.FloatField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    from_account=models.ForeignKey(Bank,on_delete=models.CASCADE,related_name='sent')
    to_account=models.ForeignKey(Bank,on_delete=models.CASCADE,related_name='received', null=True, blank=True)
    amount=models.IntegerField()
    transaction_type=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)





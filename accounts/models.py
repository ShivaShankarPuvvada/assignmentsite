from django.db import models

# Create your models here.
class Consumer(models.Model):
    mobile_number=models.CharField(max_length=20,unique=True)
    user_name=models.CharField(max_length=100,null=True)
    email=models.CharField(max_length=100, null=True, blank=True, unique=True)
    password=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.email)

class Employe(models.Model):
    name = models.CharField(max_length=100,null=True)
    age = models.PositiveSmallIntegerField()
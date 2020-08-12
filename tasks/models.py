from django.db import models


# Create your models here.

# Create your models here.
class Project(models.Model):
    consumer_id = models.IntegerField()
    name=models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.name)

class Task(models.Model):
    consumer_id = models.IntegerField()
    name=models.CharField(max_length=20,unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.name)
from django.db import models


# Create your models here.
class Wishlist(models.Model):
    name=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name)


class Container(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name)


class Movie(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    folder = models.ForeignKey(Container, on_delete=models.CASCADE, blank=True, null=True)
    title=models.CharField(max_length=255)
    url=models.URLField(max_length=255)
    released_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.title)
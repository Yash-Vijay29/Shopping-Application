from django.db import models

class Product(models.Model):
    img_url = models.URLField(blank=True, null=True)
    product_url = models.URLField(unique=True)
    rating = models.CharField(max_length=10, blank=True, null=True)
    price = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    dominant_color = models.CharField(max_length=20, blank=True, null=True)  # Add this field

    def __str__(self):
        return self.name if self.name else 'Product'
class Info(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    img_url = models.URLField(blank=True, null=True)
    price = models.CharField(max_length=20, blank=True, null=True)
    reviews = models.CharField(max_length=1000, blank=True,null=True) 

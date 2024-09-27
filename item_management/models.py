from django.db import models


# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

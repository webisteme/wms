from django.db import models
from .helpers import convert_to_ascii

# Models


class SKU(models.Model):
    product_name = models.CharField(max_length=255)


class Storage(models.Model):
    stock = models.PositiveIntegerField()
    sku = models.ForeignKey(SKU, on_delete=models.PROTECT)


class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_name_ascii = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        """
        Save an ascii version of the customer name for search
        """
        self.customer_name_ascii = convert_to_ascii(self.customer_name)
        super(Order, self).save(*args, **kwargs)


class OrderLine(models.Model):
    sku = models.ForeignKey(SKU, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.PROTECT)

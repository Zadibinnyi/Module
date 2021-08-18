from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from .exceptions import NotMuchCount, NotMuchMoney, NotZeroCount




class Costumer(AbstractUser):
    wallet = models.PositiveIntegerField(default=10000)


class Products(models.Model):
    name = models.CharField(max_length=120)
    descriptions = models.TextField(max_length=10000, blank=True, null=True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Purcase(models.Model):
    user = models.ForeignKey(Costumer, on_delete=models.CASCADE, related_name='purcase')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product')
    quantity = models.PositiveIntegerField(default=1)
    time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.quantity == 0:
            raise NotZeroCount()
        elif self.quantity > self.product.quantity:
            raise NotMuchCount()
        elif self.quantity * self.product.price > self.user.wallet:
            raise NotMuchMoney()
        elif self.product.quantity >= self.quantity and self.user.wallet >= (self.product.price * self.quantity):
            self.product.quantity -= self.quantity
            self.user.wallet -= self.product.price * self.quantity
            self.user.save()
            self.product.save()
            super(Purcase, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} from {self.user}"

class Return(models.Model):
    purcase = models.ForeignKey(Purcase, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.purcase.product} from {self.purcase.user}"

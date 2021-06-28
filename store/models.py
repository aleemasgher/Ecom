from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

User = get_user_model()


class AbstractBaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(AbstractBaseModel):
    name = models.CharField(max_length=256)
    price = models.PositiveIntegerField()
    inventory = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f'{self.name}'


class Customer(AbstractBaseModel):
    user = models.OneToOneField(User, related_name='customers', on_delete=models.CASCADE)
    wish_list = models.ManyToManyField(Product, blank=True, related_name='wish_lists')

    @property
    def last_order_date(self):
        return self.order_set.last().created_at

    @property
    def first_order_date(self):
        return self.order_set.first().created_at

    @property
    def average_order_value(self):
        orders = self.order_set.all()
        sum_of_prices = []
        for order in orders:
            sum_of_prices.append(order.product.price)
        return sum(sum_of_prices) / len(sum_of_prices)

    def __str__(self):
        return f'{self.user}'


class Order(AbstractBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'User {self.customer.user} ordered {self.product.name} on {self.created_at}'


@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, *args, **kwargs):
    if instance.product.price * instance.quantity > 1000.0:
        raise ValidationError("Price should not increase by 1000 USD.")

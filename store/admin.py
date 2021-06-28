from django.contrib import admin

from store.models import Product, Customer, Order

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)

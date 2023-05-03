from django.contrib import admin

from .models import Item, Price, Quantity

admin.site.register(Item)
admin.site.register(Price)
admin.site.register(Quantity)

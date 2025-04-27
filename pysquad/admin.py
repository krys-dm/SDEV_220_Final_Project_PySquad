from django.contrib import admin
from .models import Pizza, Order, OrderItem

admin.site.register([Pizza, Order, OrderItem])

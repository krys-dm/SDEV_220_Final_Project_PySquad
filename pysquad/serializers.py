from rest_framework import serializers
from .models import Pizza, Order, OrderItem


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['id', 'name', 'description', "price"]
        read_only_fields =[True]




class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_address', "created_at", "is_delivered"]



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'pizza', "quantity"]
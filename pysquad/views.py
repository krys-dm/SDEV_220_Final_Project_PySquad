from django.http import JsonResponse
from .models import Pizza, Order, OrderItem
from .serializers import PizzaSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])

def pizza_list(request):
    if request.method == 'GET':
        pizzas = Pizza.objects.all()
        serializer = PizzaSerializer(pizzas, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == "POST":
        serializer = PizzaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)





def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == "POST":
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


def orderItem_list(request):
    if request.method == 'GET':
        orderItem = OrderItem.objects.all()
        serializer = OrderItemSerializer(orderItem, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == "POST":
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET','PUT', 'DELETE'])
def pizza_detail(request, id):

    try:
        pizza = Pizza.objects.get(pk=id)
    except Pizza.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PizzaSerializer(pizza)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PizzaSerializer(pizza, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        pizza.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
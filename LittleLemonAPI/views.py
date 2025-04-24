from datetime import date
from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import generics, status
from .models import MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User, Group
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer, OrderSerializer
from .permissions import IsManager, ReadOnlyOrIsManager, CanAccessOrderDetails # Added CanAccessOrderDetails
from rest_framework.response import Response
from django.db import transaction

# Create your views here.
class MenuItems(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [ReadOnlyOrIsManager]

class MenuItemDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [ReadOnlyOrIsManager]

class Managers(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        manager_group = Group.objects.get(name="Manager")
        return User.objects.filter(groups=manager_group)

    def perform_create(self, serializer):
        user = serializer.save()

        manager_group = Group.objects.get(name="Manager")
        user.groups.add(manager_group)

class ManagerDetails(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        manager_group = Group.objects.get(name="Manager")
        return User.objects.filter(groups=manager_group)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.groups.clear()

        return Response(
            "Success",
            status=status.HTTP_200_OK
        )

class DeliveryCrew(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        manager_group = Group.objects.get(name="Delivery crew")
        return User.objects.filter(groups=manager_group)

    def perform_create(self, serializer):
        user = serializer.save()

        manager_group = Group.objects.get(name="Delivery crew")
        user.groups.add(manager_group)

class DeliveryCrewDetails(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        manager_group = Group.objects.get(name="Delivery crew")
        return User.objects.filter(groups=manager_group)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.groups.clear()

        return Response(
            "Success",
            status=status.HTTP_200_OK
        )

class CartMenuItems(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        Cart.objects.filter(user=self.request.user).delete()
        return Response(
            "Success",
            status=status.HTTP_200_OK
        )

class Orders(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(delivery_crew=user)
        else:
            return Order.objects.filter(user=user)

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            raise ValidationError({"detail": "Your cart is empty. Cannot place an order."})

        order_total = sum(item.price for item in cart_items)
        order = serializer.save(
            user=user,
            total=order_total,
            date=date.today(),
            status=False
        )

        order_item_instances = []
        for cart_item in cart_items:
            order_item_instances.append(
                OrderItem(
                    order=order,
                    menuitem=cart_item.menuitem,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.unit_price,
                    price=cart_item.price
                )
            )

        OrderItem.objects.bulk_create(order_item_instances)
        cart_items.delete()

class OrderDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CanAccessOrderDetails]

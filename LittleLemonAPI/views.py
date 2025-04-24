from django.shortcuts import render
from rest_framework import generics, status
from .models import MenuItem, Cart
from django.contrib.auth.models import User, Group
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer
from .permissions import IsManager, ReadOnlyOrIsManager
from rest_framework.response import Response

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
from .views import MenuItems, MenuItemDetails, Managers, ManagerDetails, DeliveryCrew, DeliveryCrewDetails, CartMenuItems, Orders, OrderDetails
"""
URL configuration for LittleLemon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

urlpatterns = [
    path('menu-items', MenuItems.as_view(), name="menu-items"),
    path('menu-items/<int:pk>', MenuItemDetails.as_view(), name="menu-item-details"),
    path('groups/managers/users', Managers.as_view(), name="managers"),
    path('groups/managers/users/<int:pk>', ManagerDetails.as_view(), name="delivery-crew-item-details"),
    path('groups/delivery-crew/users', DeliveryCrew.as_view(), name="deliver-crew"),
    path('groups/delivery-crew/users/<int:pk>', DeliveryCrewDetails.as_view(), name="delivery-crew-item-details"),
    path('cart/menu-items', CartMenuItems.as_view(), name="cart"),
    path('orders', Orders.as_view(), name="orders"),
    path('orders/<int:pk>', OrderDetails.as_view(), name="orders-details"),
]

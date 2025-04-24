from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        pw = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(pw)
        user.save()
        return user

    def update(self, instance, validated_data):
        pw = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if pw:
            user.set_password(pw)
            user.save()
        return user

class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    menuitem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    unit_price = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        read_only=True
    )
    price = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
        read_only_fields = ['id', 'menuitem', 'unit_price', 'price']

    def create(self, validated_data):
        menuitem = validated_data['menuitem']
        quantity = validated_data.get('quantity', 1)
        validated_data['unit_price'] = menuitem.price
        validated_data['price'] = menuitem.price * quantity
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'quantity' in validated_data:
            instance.quantity = validated_data['quantity']
            instance.price = instance.unit_price * instance.quantity
            instance.save()
        return instance

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    unit_price = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        read_only=True
    )
    price = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']
        read_only_fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    orderitem_set = OrderItemSerializer(read_only=True, many=True)

    delivery_crew = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='Delivery crew'),
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'orderitem_set']
        read_only_fields = ['id', 'total', 'date', 'orderitem_set']

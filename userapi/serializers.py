from admin1.models import Customer,Food,Review,Order,Cart,CartItem,Category
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Customer
        fields=["id","username","date_of_birth","profile_picture","bio","address","password"]

    def create(self, validated_data):
        return Customer.objects.create_user(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"
        
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Food
        fields="__all__"
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields="__all__"
        
class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields="__all__"
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields="__all__"

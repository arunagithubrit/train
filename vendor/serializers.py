from rest_framework import serializers
from admin1.models import Category,Food,Cart,Offer,Order,Review,Vendor,Customer,CartItem
# from django.contrib.auth.models import User



class VendorSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Vendor
        fields=["id","username","email","password","phone","name","description","address","website","logo"]
    # def create(self, validated_data):
    #     user = UserSignup(
    #         email=validated_data['email'],
    #         username=validated_data['username']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
    def create(self, validated_data):
        return Vendor.objects.create_user(**validated_data)
    
class CategorySerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    is_active=serializers.BooleanField(read_only=True)
    class Meta:
        model = Category
        fields =["id","name","is_active"]


class FoodSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    category=serializers.CharField(read_only=True)
    is_active=serializers.BooleanField(read_only=True)
    class Meta:
        model = Food
        fields = ["id","name","description","price","image","is_active","category"]
    




class OfferSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    food=serializers.CharField(read_only=True)
    vendors=serializers.CharField(read_only=True)
    price=serializers.CharField(read_only=True)
    start_date=serializers.CharField(read_only=True)
    due_date=serializers.CharField(read_only=True)
    class Meta:
        model = Offer
        fields = '__all__'
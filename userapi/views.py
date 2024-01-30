from django.shortcuts import render
from admin1.models import Customer,Food,Review,Order,Cart,CartItem,Category
from userapi.serializers import CustomerSerializer,CategorySerializer,FoodSerializer,CartSerializer,CartItemsSerializer,ReviewSerializer,OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.decorators import action
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import serializers
from django.utils import timezone


# Create your views here.

class CustomerCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="customer")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
class CategoryView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = CategorySerializer
        
    def list(self,request,*args,**kwargs):
        qs=Category.objects.filter(is_active=True)
        serializer=CategorySerializer(qs,many=True)
        return Response(data=serializer.data)
    
class FoodView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = FoodSerializer
        
    def list(self,request,*args,**kwargs):
        qs=Food.objects.filter(is_active=True)
        serializer=FoodSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["post"],detail=True)
    def add_to_cart(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        food_object=Food.objects.get(id=id) 
        cart_object=request.user.customer.cart

        serializer=CartItemsSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(cart=cart_object,food=food_object,is_active=True)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    
    @action(methods=["post"],detail=True)
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        food_object=Food.objects.get(id=id) 
        user=request.user.customer
        serializer=ReviewSerializer(data=request.data)
        

        if serializer.is_valid():
            serializer.save(user=user,food=food_object)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)

        
    
class CartView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = CartSerializer
        
    def list(self,request,*args,**kwargs):
        user=request.user.customer
        qs=Cart.objects.filter(user=user)
        serializer=CartSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["post"],detail=True)
    def place_order(self,request,*args,**kwargs):
        cart_object=request.user.customer.cart
        user=request.user.customer
        serializer=OrderSerializer(data=request.data)
        

        if serializer.is_valid():
            serializer.save(user=user,cart=cart_object)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    






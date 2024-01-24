from django.shortcuts import render
from admin1.models import Customer,Food,Review,Order,Cart,CartItem,Category
from userapi.serializers import CustomerSerializer,CategorySerializer,FoodSerializer,CartSerializer,CartItemsSerializer,ReviewSerializer
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
            serializer.save(user_type="vendor")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)





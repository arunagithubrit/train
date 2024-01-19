from django.shortcuts import render
from rest_framework import mixins,generics
from vendor.serializers import VendorSerializer,CategorySerializer,FoodSerializer,OfferSerializer
from admin1.models import Vendor,Category,Food,Offer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.decorators import action
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import serializers

from django.shortcuts import render
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

class VendorCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="vendor")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


# class VendorListCreateView(generics.ListCreateAPIView):
#     authentication_classes=[authentication.TokenAuthentication]
#     permission_classes=[permissions.IsAuthenticated]
#     queryset = Vendor.objects.all()
#     serializer_class = VendorSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

  
   
# http://127.0.0.1:8000/vendor/foods/1
class FoodView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class = FoodSerializer
    def create(self,request,*args,**kwargs):
        cid=kwargs.get("pk")
        category_obj=Category.objects.get(id=cid)
        user=request.user
        serializer=OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(category=category_obj,vendors=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    def list(self,request,*args,**kwargs):
        qs=Food.objects.all()
        serializer=FoodSerializer(qs,many=True)
        return Response(data=serializer.data)
        
    
        



class OfferView(ViewSet):
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=OfferSerializer
# http://127.0.0.1:8000/vendor/foods/2/offers
    def create(self,request,*args,**kwargs):
        vid=kwargs.get("pk")
        varient_obj=Food.objects.get(id=vid)
        user=request.user
        serializer=OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(food=varient_obj,vendors=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    # def list(self,request,*args,**kwargs):
    #     qs=Carts.objects.filter(user=request.user)
    #     serializer=CartSerializer(qs,many=True)
    #     return Response(data=serializer.data)
    
    # def destroy(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     instance=Carts.objects.get(id=id)
    #     if instance.user==request.user:
    #         instance.delete()
    #         return Response(data={"msg":"deleted"})
    #     else:
    #         return Response(data={"message":"permission denied"})

    
 

   
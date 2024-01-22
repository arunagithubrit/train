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




# class CategoryListCreateView(generics.ListCreateAPIView):
#     authentication_classes=[authentication.TokenAuthentication]
#     permission_classes=[permissions.IsAuthenticated]
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

class CategoryView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    
    def create(self,request,*args,**kwargs):
        serializer=CategorySerializer(data=request.data)
        vendor_id=request.user.id
        print(vendor_id)
        vendor_object=Vendor.objects.get(id=vendor_id)
        if vendor_object:
            if serializer.is_valid():
                serializer.save(vendors=vendor_object)
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        else:
            return Response(request,"vendor not found")
        
    def list(self,request,*args,**kwargs):
        vendor_id=request.user.id
        vendor_object=Vendor.objects.get(id=vendor_id)
        qs=Category.objects.filter(vendors=vendor_object)
        serializer=CategorySerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Category.objects.get(id=id)
        serializer=CategorySerializer(qs)
        return Response(data=serializer.data)
    
    

    
    def destroy(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        category = Category.objects.get(id=id)
        category.is_active = False
        category.save()
        return Response(data={"message": "category is now inactive"})
    # http://127.0.0.1:8000/vendor/foods/1
    @action(methods=["post"],detail=True)
    def add_food(self,request,*args,**kwargs):
        serializer=FoodSerializer(data=request.data)
        cat_id=kwargs.get("pk")
        category_obj=Category.objects.get(id=cat_id)
        vendor=request.user.id
        vendor_object=Vendor.objects.get(id=vendor) 
        if serializer.is_valid():
            serializer.save(category=category_obj,vendor=vendor_object,is_active=True)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
   

class FoodView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = FoodSerializer

    
        
    def list(self,request,*args,**kwargs):
        qs=Food.objects.filter(vendor=request.user.vendor)
        serializer=FoodSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        instance=Food.objects.get(id=id)
        if instance.vendor==request.user.vendor:
            instance.delete()
            return Response(data={"msg":"deleted"})
        else:
            return Response(data={"message":"permission denied"})

    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Food.objects.get(id=id)
        serializer=FoodSerializer(qs)
        return Response(data=serializer.data)
        
    
        



# class OfferView(ViewSet):
#     # authentication_classes=[authentication.BasicAuthentication]
#     authentication_classes=[authentication.TokenAuthentication]
#     permission_classes=[permissions.IsAuthenticated]
#     serializer_class=OfferSerializer
# # http://127.0.0.1:8000/vendor/foods/2/offers
#     def create(self,request,*args,**kwargs):
#         vid=kwargs.get("pk")
#         varient_obj=Food.objects.get(id=vid)
#         user=request.user
#         serializer=OfferSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(food=varient_obj,vendors=user)
#             return Response(data=serializer.data)
#         else:
#             return Response(data=serializer.errors)

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

    
 

   
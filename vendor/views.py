from django.shortcuts import render
from rest_framework import mixins,generics
from vendor.serializers import VendorSerializer,CategorySerializer,FoodSerializer,OfferSerializer,ReviewSerializer,OrderSerializer,TrainLiveStatusRequestSerializer
from admin1.models import Vendor,Category,Food,Offer,Review,Order
from rest_framework.views import APIView,View
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.decorators import action
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import serializers
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
import requests
from datetime import datetime
from django.contrib.auth import logout



from django.shortcuts import render
from rest_framework.response import Response




class VendorCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="vendor")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)



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
    
    def update(self,request,*args,**kwargs): 
        id=kwargs.get("pk")
        obj=Food.objects.get(id=id)
        serializer=FoodSerializer(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    
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
    
    @action(methods=["post"],detail=True)
    def offer_add(self,request,*args,**kwargs):
        serializer=OfferSerializer(data=request.data)
        food_id=kwargs.get("pk")
        food_obj=Food.objects.get(id=food_id)
        vendor=request.user.id
        vendor_object=Vendor.objects.get(id=vendor) 
        if serializer.is_valid():
            serializer.save(food=food_obj,vendors=vendor_object)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    @action(methods=["get"],detail=True)  
    def review_list(self,request,*args,**kwargs):
        food_id=kwargs.get("pk")
        food_obj=Food.objects.get(id=food_id)
        qs=Review.objects.filter(food=food_obj)
        serializer=ReviewSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["get"],detail=True)
    def order_list(self,request,*args,**kwargs):
        food_id=kwargs.get("pk")
        food_obj=Food.objects.get(id=food_id)
        qs=Order.objects.filter(food=food_obj)
        serializer=OrderSerializer(qs,many=True)
        return Response(data=serializer.data)
        

class OfferView(ViewSet):
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=OfferSerializer


    def list(self,request,*args,**kwargs):
        qs=Offer.objects.filter(vendors=request.user.vendor,due_date__gte=timezone.now())
        serializer=OfferSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        instance=Offer.objects.get(id=id)
        if instance.vendors==request.user.vendor:
            instance.delete()
            return Response(data={"msg":"offer deleted"})
        else:
            return Response(data={"message":"permission denied"})
        
        
class GetTrainIdView(View):
    def get(self, request, *args, **kwargs):
        url = "https://indian-railway-irctc.p.rapidapi.com/getTrainId"
        train_number = request.GET.get('trainno', '')
        querystring = {"trainno": train_number}

        headers = {
            "x-rapid-api": "rapid-api-database",
            "X-RapidAPI-Key": "7297778c0emsh0efeeaedca5c471p1eeae2jsnd95fc2907057",
            "X-RapidAPI-Host": "indian-railway-irctc.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            response_json = response.json()
        except requests.RequestException as e:
            return JsonResponse({'error': f'Failed to make API request: {str(e)}'}, status=500)
        except ValueError:
            return JsonResponse({'error': 'Failed to parse API response as JSON'}, status=500)

        if isinstance(response_json, dict):
            train_id = response_json.get('train_id', None)

            if train_id:
                redirect_url = reverse('get_train_live_status') 
                redirect_url += f'?id={train_id}'
                return redirect(redirect_url)
            else:
                return JsonResponse({'error': 'Train ID not found in the response'}, status=400)
        else:
            return JsonResponse({'error': 'Unexpected API response format'}, status=500)
        
               
class GetTrainLiveStatusView(View):
    def get(self, request, *args,**kwargs):
        serializer = TrainLiveStatusRequestSerializer(data=request.GET)
        if serializer.is_valid():
            train_id = serializer.validated_data['id']
            date = serializer.validated_data['date'].strftime('%d-%m-%Y')
        else:
            return JsonResponse({'error': 'Invalid request data'}, status=400)

        url = "https://indian-railway-irctc.p.rapidapi.com/getTrainLiveStatusById"
        querystring = {"id": train_id, "date": date}
        headers = {
            "x-rapid-api": "rapid-api-database",
            "X-RapidAPI-Key": "7297778c0emsh0efeeaedca5c471p1eeae2jsnd95fc2907057",
            "X-RapidAPI-Host": "indian-railway-irctc.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        print(f"Request URL: {response.url}")
        print(f"Request Headers: {response.request.headers}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            serializer = TrainLiveStatusRequestSerializer(data=response.json())
            if serializer.is_valid():
                return JsonResponse(serializer.validated_data)
            else:
                return JsonResponse({'error': 'Failed to deserialize API response'}, status=500)
        else:
            return JsonResponse({'error': 'Failed to fetch train live status'}, status=response.status_code)
        
def sign_out(request):
    logout(request)
    return render("signin")
          


    
 

   
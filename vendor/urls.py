from django.urls import path
from vendor import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("foods",views.FoodView,basename="foods")
# router.register("offers",views.OfferView,basename="offers")
router.register("category",views.CategoryView,basename="category")

urlpatterns=[
    path("register/",views.VendorCreationView.as_view(),name="signin"),
    path("token/",ObtainAuthToken.as_view(),name="token"),
  
    
]+router.urls



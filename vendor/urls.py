from django.urls import path
from vendor import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
# router.register("foods",views.FoodView,basename="foods")
router.register("offers",views.OfferView,basename="offers")

urlpatterns=[
    path("register/",views.VendorCreationView.as_view(),name="signin"),
    path("token/",ObtainAuthToken.as_view(),name="token"),
    path("category/add",views.CategoryListCreateView.as_view(),name="category-add"),
    path("category/all",views.CategoryListCreateView.as_view(),name="category-list"),
    
]+router.urls



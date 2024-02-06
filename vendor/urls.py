from django.urls import path
from vendor import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter
from vendor.views import GetTrainIdView,GetTrainLiveStatusView

router=DefaultRouter()
router.register("foods",views.FoodView,basename="foods")
router.register("offers",views.OfferView,basename="offers")
router.register("category",views.CategoryView,basename="category")
# router.register("reviews",views.ReviewView,basename="review")

urlpatterns=[
    path("register/",views.VendorCreationView.as_view(),name="signin"),
    path("token/",ObtainAuthToken.as_view(),name="token"),
    path('get_train_id/', GetTrainIdView.as_view(), name='get_train_id'),
    path('get_train_live_status/',GetTrainLiveStatusView.as_view(), name='get_train_live_status'),
    path("logout/",views.sign_out,name="logout"),
    
    
    
  
    
]+router.urls



from django.contrib import admin
from admin1.models import Category,Food,Vendor,Customer,Cart,CartItem,Review,Order
# Register your models here.
admin.site.register(Category)
admin.site.register(Food)
admin.site.register(Vendor)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Review)
admin.site.register(Order)
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user_type_choices=[
        ('customer', 'customer'),
        ('vendor' ,'vendor'),
    ]
    user_type=models.CharField(max_length=50,choices=user_type_choices,default='customer')
    phone=models.CharField(max_length=10,unique=True)



class Vendor(CustomUser):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=200,null=True)
    # email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=200,null=True)
    website = models.URLField(null=True)
    logo = models.ImageField(upload_to='images',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Customer(CustomUser):
    name=models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='images', null=True, blank=True)
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)


    # Add other fields based on your requirements

    def __str__(self):
        return self.name
   


class Category(models.Model):
    name=models.CharField(max_length=200,unique=True)
    vendors = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Food(models.Model):
    name=models.CharField(max_length=200)
    vendors = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    image=models.ImageField(upload_to="images")
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=500)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Offer(models.Model):
    food=models.ForeignKey(Food,on_delete=models.CASCADE)
    vendors = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True)
    price=models.PositiveIntegerField()
    start_date=models.DateTimeField()
    due_date=models.DateTimeField()
    
class Cart(models.Model):
    
    user=models.OneToOneField(Customer,on_delete=models.CASCADE,related_name="cart")
    options=(
        ("in-cart","in-cart"),
        ("order-placed","order-placed"),
        ("cancelled","cancelled")
    )

    status=models.CharField(max_length=200,choices=options,default="in-cart")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cartitem") 
    food=models.ForeignKey(Food,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)



class Order(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    train_no=models.CharField(max_length=100)
    food=models.ForeignKey(Food,on_delete=models.CASCADE)
    options=(
      
        ("order-placed","order-placed"),
        ("cancelled","cancelled"),
        ("dispatced","dispatched"),
        ("in-transit","in-transit"),
        ("delivered","delivered")
    )
    status=models.CharField(max_length=200,choices=options,default="order-placed")
    orderd_date=models.DateTimeField(auto_now_add=True)
    expected_date=models.DateField(null=True)
    coach_no=models.CharField(max_length=100)
    seatno=models.CharField(max_length=100,unique=True)

from django.core.validators import MinValueValidator,MaxValueValidator

class Review(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    food=models.ForeignKey(Food,null=True,on_delete=models.SET_NULL)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=300)




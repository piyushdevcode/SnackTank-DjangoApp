from operator import truediv
from pyexpat import model
from re import L
from uuid import UUID, uuid3
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import uuid
from django.db.models import Sum

class User(AbstractUser):
    pass


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class FoodCategory(BaseModel):
    category_name = models.CharField(max_length = 100)

    def __str__(self) -> str:
        return self.category_name

    class Meta:
        verbose_name_plural = 'Food Categories'

class FoodItems(BaseModel):
    category = models.ForeignKey(FoodCategory,on_delete=models.CASCADE,related_name='fooditems')
    item_name  = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(upload_to='fooditems/')
    stock = models.PositiveIntegerField(default=50)

    def __str__(self) -> str:
        return f'{self.item_name} | {self.category}'

    class Meta:
        verbose_name_plural = 'Food Items'


class Cart(BaseModel):
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name='carts')
    is_paid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user.username} | paid: {self.is_paid}'
    
    def get_cart_total(self):
        return CartItems.objects.filter(cart=self).aggregate(Sum('food_item__price'))['food_item__price__sum']

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    food_item = models.ForeignKey(FoodItems,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self) -> str:
        return f'{self.cart.user.username} | {self.food_item} | {self.quantity}'


    class Meta:
        verbose_name_plural = 'Cart Items'

from django.contrib import admin
from .models import *
# Register your models here.
class FoodItemAdmin(admin.ModelAdmin):
    list_filter =['category']
admin.site.register(User)
admin.site.register(FoodItems,FoodItemAdmin)
admin.site.register(FoodCategory)
admin.site.register(Cart)
admin.site.register(CartItems)

from rest_framework import serializers
from homepage.models import *

class FoodItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItems
        fields = "__all__"
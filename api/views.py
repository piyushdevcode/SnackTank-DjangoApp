from rest_framework import viewsets,permissions
from api.serializers import *

class FoodItemsViewSet(viewsets.ModelViewSet):
    """
    Allows view of all the Food items
    """

    queryset = FoodItems.objects.all()
    serializer_class = FoodItemsSerializer


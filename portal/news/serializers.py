from rest_framework import serializers
from .models import Category


class CategorySerializers(serializers.Serializer):
    name = serializers.CharField(max_length=255)



# class CategorySerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['name']

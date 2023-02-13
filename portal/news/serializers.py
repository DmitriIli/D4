from rest_framework import serializers
from .models import Category

### сериализация под капотом ###
class CategorySerializers(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    
    ###Создание сериализованного объекта###
    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    ###Изменение объекта###
    def update(self, instance, validated_data):
        instance.name =  validated_data.get('name', instance.name)
        instance.save()
        return instance

   
class CategoryModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

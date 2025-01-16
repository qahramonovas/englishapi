from rest_framework.serializers import CharField
from rest_framework.serializers import ModelSerializer

from apps.models import Unit
from apps.serializers import BookModelSerializer


class UnitModelSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class UnitSearchModelSerializer(ModelSerializer):
    search_value = CharField(max_length=255 , write_only=True)
    class Meta:
        model=Unit
        fields = "__all__"
        read_only_fields = "name" , "unit_num" , "book"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data['book'] = Book.objects.filter(id=data.get('book')).values('id' , 'name' , 'level').first()
        data['book'] = BookModelSerializer(instance=instance.book).data
        return data


class UnitFilterModelSerializer(ModelSerializer):
    class Meta:
        model = Unit
        exclude = ['book']

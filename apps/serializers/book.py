from rest_framework.serializers import ModelSerializer

from apps.models import Book


class BookModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'




class BookSearchModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        exclude = "image",
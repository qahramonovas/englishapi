from http import HTTPStatus

from celery.bin.control import status
from django.db.models import Q
from django.http import JsonResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import UpdateAPIView, DestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Book, Vocabulary
from apps.serializers import BookModelSerializer, BookSearchModelSerializer


@extend_schema(
    tags=['Book']
)
class BookListAPIView(APIView):
    def get(self, request):
        units = Book.objects.all()
        serializer = BookModelSerializer(units, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=['Book']
)
class BookUpdateAPIView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "message": "updated successfully",
            "data": serializer.data
        }, status=HTTPStatus.OK)

    def perform_update(self, serializer):
        serializer.save()


@extend_schema(
    tags=['Book']
)
class BookDeleteAPIView(DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({
            "message": "deleted successfully."
        }, status=HTTPStatus.OK)

    def perform_destroy(self, instance):
        instance.delete()


# ----------


@extend_schema(
    tags=['Book']
)
class BookCreateAPIView(CreateAPIView):
    serializer_class = BookModelSerializer
    queryset = Book.objects.all()








# ==================================






@extend_schema(
    tags=['Book']
)
class BookSearchListAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSearchModelSerializer

    def get_queryset(self):
        value = self.request.query_params.get('search_value').strip()
        query = super().get_queryset()
        # query = Book.objects.all()
        if value:
            query = query.filter(
                Q(name__icontains=value)|Q(level__icontains=value)
            )
        return query

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='search_value',
                type=OpenApiTypes.STR,
                required=True
            ),
        ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@extend_schema(
    tags=['Book']
)
class BookInfoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        book_id = request.GET.get('id')
        book = Book.objects.get(id=book_id)
        serializer = BookModelSerializer(book)
        return Response(serializer.data)

@extend_schema(
    request=BookModelSerializer,
    tags=['Book']
)
class BookInfoAPIView(APIView):
    def get(self, request , pk):
        book = Book.objects.filter(id=pk)
        serializer = BookModelSerializer(book , many=True)
        return JsonResponse(serializer.data  ,safe=False)




# ================================================
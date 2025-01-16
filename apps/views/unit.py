from http import HTTPStatus

from django.db.models import Q
from django.http import JsonResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListAPIView
from rest_framework.generics import UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Unit
from apps.serializers import UnitModelSerializer, UnitSearchModelSerializer, UnitFilterModelSerializer


@extend_schema(
    tags=['Unit']
)
class UnitListAPIView(APIView):
    def get(self, request):
        units = Unit.objects.all()
        serializer = UnitModelSerializer(units, many=True)
        return Response(serializer.data)


# ------

@extend_schema(
    tags=['Unit']
)
class UnitUpdateAPIView(UpdateAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "message": "Topic updated successfully",
            "data": serializer.data
        }, status=HTTPStatus.OK)

    def perform_update(self, serializer):
        serializer.save()


# ---------


@extend_schema(
    tags=['Unit']
)
class UnitDeleteAPIView(DestroyAPIView):
    queryset = Unit.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({
            "message": f"'{instance.unit}' has been deleted successfully."
        }, status=HTTPStatus.OK)

    def perform_destroy(self, instance):
        instance.delete()


# ----------



@extend_schema(
    tags=['Unit']
)
class UnitCreateAPIView(CreateAPIView):
    serializer_class = UnitModelSerializer
    queryset = Unit.objects.all()




# ======================================================


@extend_schema(
    tags=['Unit']
)
class UnitSearchListAPIView(ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSearchModelSerializer

    def get_queryset(self):
        value = self.request.query_params.get('search_value').strip()
        query = super().get_queryset()
        # query = Unit.objects.all()
        if not value.isdigit():
            query = query.filter(
                Q(name__icontains=value)|Q(book__name__icontains=value)|Q(book__level__icontains=value)
            )
        else:
            query = query.filter(
                Q(unit_num=int(value))
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
    tags=['Unit']
)
class UnitFilterListAPIView(ListAPIView):
    queryset = Unit.objects.all()
    serializer_class =UnitFilterModelSerializer

    def get_queryset(self):
        query  = super().get_queryset()
        book_id = self.kwargs.get("book_id")
        return query.filter(book_id = book_id)




@extend_schema(
    request=UnitModelSerializer,
    tags=['Unit']
)
class UnitInfoAPIView(APIView):
    def get(self, request , pk):
        book = Unit.objects.filter(id=pk)
        serializer = UnitModelSerializer(book , many=True)
        return JsonResponse(serializer.data  ,safe=False)













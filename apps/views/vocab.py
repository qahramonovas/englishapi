import json
import random
from http import HTTPStatus
from random import shuffle

from django.db.models import Q
from django.http import JsonResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from redis import Redis
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Vocabulary, Result, Unit
from apps.serializers import VocabModelSerializer, VocabFilterModelSerializer, VocabularyUpdateModelSerializer, \
    VocabSearchModelSerializer, VocabTryWordSerializer, VocabCheckWordSerializer, VocabTestSerializer


@extend_schema(tags=['Vocab'])
class VocabCreateAPIView(CreateAPIView):
    queryset = Vocabulary.objects.all()
    serializer_class =VocabModelSerializer
    # parser_classes = [MultiPartParser , FormParser]





@extend_schema(
    tags=['Vocab']
)
class VocabularyUpdateAPIView(UpdateAPIView):
    queryset = Vocabulary.objects.all()
    serializer_class = VocabularyUpdateModelSerializer
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



@extend_schema(
    tags=['Vocab']
)
class VocabFilterListAPIView(ListAPIView):
    queryset = Vocabulary.objects.all()
    serializer_class = VocabFilterModelSerializer

    def get_queryset(self):
        query  = super().get_queryset()
        unit_id = self.kwargs.get("unit_id")
        return query.filter(unit_id = unit_id)


@extend_schema(
    tags=['Vocab']
)
class VocabDeleteAPIView(DestroyAPIView):
    queryset = Vocabulary.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({
            "message": f"'{instance.unit}' has been deleted successfully."
        }, status=HTTPStatus.OK)

    def perform_destroy(self, instance):
        instance.delete()




@extend_schema(
    tags=['Vocab']
)
class VocabListAPIView(APIView):
    def get(self, request):
        units = Vocabulary.objects.all()
        serializer = VocabModelSerializer(units, many=True)
        return Response(serializer.data)





# ==========================


@extend_schema(
    tags=['Vocab']
)
class VocabSearchListAPIView(ListAPIView):
    queryset = Vocabulary.objects.all()
    serializer_class = VocabSearchModelSerializer

    def get_queryset(self):
        value = self.request.query_params.get('search_value').strip()
        # query = super().get_queryset()
        query = Vocabulary.objects.all()
        if value:
            query = query.filter(
                Q(en__icontains=value)|Q(uz__icontains=value)
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
    request=VocabModelSerializer,
    tags=['Vocab']
)
class VocabInfoAPIView(APIView):
    def get(self, request, pk):
        book = Vocabulary.objects.filter(id=pk)
        serializer = VocabModelSerializer(book, many=True)
        return JsonResponse(serializer.data, safe=False)









class VocabTryWordAPIView(APIView):
    @extend_schema(
        request=VocabTryWordSerializer,
        responses=VocabFilterModelSerializer,
        tags=['Vocab']
    )
    def post(self, request):
        unit_id = request.data.get('unit_id')
        redis = Redis(decode_responses=True)
        vocabs = list(Vocabulary.objects.filter(unit_id=unit_id).values_list('id', flat=True))
        if not vocabs:
            raise ValidationError("Vocab not found!", HTTPStatus.BAD_REQUEST)
        random_vocab = random.choice(vocabs)
        vocabs.remove(random_vocab)
        data = {'correct': 0, 'incorrect': 0, 'unit_id': unit_id, 'vocabs_id': vocabs, 'finish': False}
        redis.set(request.user.id , json.dumps(data))
        vocab = Vocabulary.objects.filter(id=random_vocab).first()
        data = VocabFilterModelSerializer(instance=vocab).data
        return Response(data=data, status=HTTPStatus.OK)

class VocabCheckWordAPIView(APIView):
    @extend_schema(
        request=VocabCheckWordSerializer,
        responses=VocabFilterModelSerializer,
        tags=['Vocab']
    )
    def post(self, request):
        vocab_id = request.data.get('vocab_id')
        word = request.data.get('word')
        vocab = Vocabulary.objects.filter(id=vocab_id).first()
        is_correct = vocab.en.lower() == word.lower()
        redis = Redis(decode_responses=True)
        data = redis.get(request.user.id)
        data = json.loads(data)
        data['correct'] += is_correct
        data['incorrect'] += not is_correct
        if not data['vocabs_id']:
            data['finish'] = True
            data['last_question'] = is_correct
            redis.delete(request.user.id)
            return Response(data, HTTPStatus.OK)
        vocabs_id = data['vocabs_id']
        r = random.choice(vocabs_id)
        vocabs_id.remove(r)
        redis.set(request.user.id, json.dumps(data))
        vocab = Vocabulary.objects.filter(id=r).first()
        data = VocabFilterModelSerializer(instance=vocab).data
        data['finish'] = False
        data['last_question'] = is_correct
        return Response(data=data, status=HTTPStatus.OK)




# ======================================================================

class VocabTestAPIView(APIView):
    @extend_schema(
        request=VocabTestSerializer,
        tags=['Vocab']
    )
    def post(self,request):
        type = request.data.get("type")
        quantity = int(request.data.get("quantity"))
        units = request.data.get("units").split(",")
        redis = Redis(decode_responses=True)
        vocabs = list(Vocabulary.objects.filter(unit_id__in=units).values_list('id', flat=True))
        shuffle(vocabs)
        vocabs = vocabs[:quantity]
        if not vocabs:
            raise ValidationError(detail="Vocab not found" )
        random_vocab = random.choice(vocabs)
        vocabs.remove(random_vocab)
        r_data = {"correct": 0, "incorrect": 0, "units": units, "vocabs_id": vocabs, "finish": False, 'type': type}
        redis.set(request.user.id, json.dumps(r_data))
        vocab = Vocabulary.objects.filter(id=random_vocab).first()
        data = VocabModelSerializer(instance=vocab).data
        data['type'] = data.get('type')
        return Response(data=data, status=HTTPStatus.OK)






class VocabTestCheckAPIView(APIView):
    @extend_schema(
        request=VocabCheckWordSerializer,
        responses=VocabSearchModelSerializer,
        tags=['Vocab']
    )
    def post(self, request):
        vocab_id = request.data.get('vocab_id')
        word = request.data.get('word')
        vocab = Vocabulary.objects.filter(id=vocab_id).first()
        is_correct = vocab.en.lower() == word.lower()
        redis = Redis(decode_responses=True)
        r_data = redis.get(request.user.id)
        r_data = json.loads(r_data)
        r_data['correct'] += is_correct
        r_data['incorrect'] += not is_correct
        vocabs_id = r_data['vocabs_id']
        if not vocabs_id:
            del r_data['finish']
            del r_data['vocabs_id']
            redis.delete(request.user.id)
            r_data['user'] = request.user
            units = Unit.objects.filter(id__in=r_data.get("units"))
            del r_data['units']
            r_data['quantity'] = r_data.get('quantity')
            instance = Result.objects.create(**r_data)
            instance.units.add(*units)
            r_data['finish'] = True
            r_data['last_question'] = is_correct
            del r_data['user']
            return Response(r_data, HTTPStatus.OK)
        r = random.choice(vocabs_id)
        vocabs_id.remove(r)
        redis.set(request.user.id, json.dumps(r_data))
        vocab = Vocabulary.objects.filter(id=r).first()
        data = VocabModelSerializer(instance=vocab).data
        data['finish'] = False
        data['last_question'] = is_correct
        data['type'] = r_data.get('type')
        return Response(data, status=HTTPStatus.OK)


from rest_framework.fields import IntegerField, CharField, ListField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import Vocabulary, Unit
from apps.utils import generate_audio_world


class VocabModelSerializer(ModelSerializer):
    class Meta:
        model = Vocabulary
        exclude = ()
        extra_kwargs = {
            "id" : {"read_only" : True},
            "audio_file": {"read_only" : True}
        }

    def validate(self, attrs):
        en = attrs.get('en')
        path = generate_audio_world(en)
        attrs['audio_file'] = path
        return attrs


class VocabFilterModelSerializer(ModelSerializer):
    class Meta:
        model = Vocabulary
        exclude = ['audio_file','unit']


class VocabularyUpdateModelSerializer(ModelSerializer):
    class Meta:
        model = Vocabulary
        fields = '__all__'



class VocabSearchModelSerializer(ModelSerializer):
    class Meta:
        model = Vocabulary
        fields = '__all__'


class VocabTryWordSerializer(Serializer):
    unit_id = IntegerField()


class VocabCheckWordSerializer(Serializer):
    vocab_id = IntegerField()
    word = CharField()



class VocabTestSerializer(Serializer):
    type = CharField()
    quantity = IntegerField()
    units = PrimaryKeyRelatedField(
        queryset=Unit.objects.all(),
        many=True
    )


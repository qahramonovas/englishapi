from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextChoices, PositiveIntegerField, EmailField, Model, ImageField, IntegerField, \
    ForeignKey, CASCADE, FileField, TextField, SET_NULL, SmallIntegerField, DateTimeField, ManyToManyField


class CustomUserManager(BaseUserManager):
    def _create_user(self,  email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        email = GlobalUserModel.normalize_username(email)
        user = self.model( email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user( email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user( email, password, **extra_fields)



class User(AbstractUser):
    class UserRole(TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'
    objects = CustomUserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    email = EmailField(unique=True)
    role = CharField(max_length=255, choices=UserRole.choices, default=UserRole.USER)
    rank = PositiveIntegerField(default=0)




class Book(Model):
    name = CharField(max_length=255)
    level = CharField(max_length=255)
    image = ImageField(upload_to='book/')


class Unit(Model):
    name = CharField(max_length=255)
    unit_num = PositiveIntegerField(default=0)
    book = ForeignKey('apps.Book', CASCADE, related_name='books')


class Vocabulary(Model):
    en = CharField(max_length=255)
    uz = CharField(max_length=255)
    unit= ForeignKey('apps.Unit', CASCADE, related_name='units')
    audio_file = FileField(upload_to='audio-files/')



class TestSection(Model):
    title = CharField(max_length=255)
    description = TextField()


class Test(Model):
    class OptionTest(TextChoices):
        A = 'a' , "A"
        B = 'b' , "B"
        C = 'c' , "C"
        D = 'd' , "D"
    question = TextField()
    a = CharField(max_length=255)
    b = CharField(max_length=255)
    c = CharField(max_length=255)
    d = CharField(max_length=255)
    right = CharField(max_length=255 , choices=OptionTest.choices)
    section_test = ForeignKey('apps.TestSection' , CASCADE , related_name='tests')


class Result(Model):
    class ResultType(TextChoices):
        TEST = 'test' , 'Test'
        VOCAB_TEXT = 'text' , 'Text'
        VOCAB_AUDIO = 'audio' , 'Audio'
        LISTENING = 'listening' , 'Listening'
        WRITING = 'writing' , 'Writing'
        READING = 'reading' , 'Reading'
        SPEAKING = 'speaking' , 'Speaking'
    user = ForeignKey('apps.User' , SET_NULL ,null=True , blank=True, related_name='results')
    correct = SmallIntegerField(default=0)
    incorrect = SmallIntegerField(default=0)
    quantity = SmallIntegerField(null=True, blank=True)
    type = CharField(max_length=255 , choices=ResultType.choices)
    created_at = DateTimeField(auto_now_add=True)
    units = ManyToManyField('apps.Unit' , related_name='results')
    test_sections = ManyToManyField('apps.TestSection' , related_name='results' )
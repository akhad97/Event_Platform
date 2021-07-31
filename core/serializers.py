from django.db.models import query
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import BaseUserManager
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model, password_validation
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from rest_framework.serializers import ModelSerializer

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',  'full_name', 'email', 'phone_number', 'address', 'organization', 'gender', 'date_of_birth', 'photo', 'password', 'is_participant', 'is_organizer')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'email', 'phone_number', 'gender', 'date_of_birth', 'photo', 'address', 'organization', 'created_at', 'updated_at')



class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
    phone_number = serializers.CharField()
    address = serializers.CharField()
    organization = serializers.ChoiceField(choices=EDUCATION)
    gender = serializers.ChoiceField(choices=GENDER)
    date_of_birth = serializers.DateField()
    photo = serializers.ImageField()
    is_participant = serializers.BooleanField()
    is_organizer = serializers.BooleanField()

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'phone_number', 'date_of_birth', 'photo', 'address', 'organization', 'gender', 'password', 'is_participant', 'is_organizer')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'full_name': self.validated_data.get('full_name', ''),
            'email': self.validated_data.get('email', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'address': self.validated_data.get('address', ''),
            'organization': self.validated_data.get('organization', ''),
            'gender': self.validated_data.get('gender', ''),
            'dtae_of_birth': self.validated_data.get('dtae_of_birth', ''),
            'photo': self.validated_data.get('photo', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'is_participant': self.validated_data.get('is_participant', ''),
            'is_organizer': self.validated_data.get('is_organizer', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.full_name = self.cleaned_data.get('full_name')
        user.email = self.cleaned_data.get('email')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.address = self.cleaned_data.get('address')
        user.organization = self.cleaned_data.get('organization')
        user.gender = self.cleaned_data.get('gender')
        user.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.photo = self.cleaned_data.get('photo')
        user.is_participant = self.cleaned_data.get('is_participant')
        user.is_organizer = self.cleaned_data.get('is_organizer')
        user.save()
        adapter.save_user(request, user, self)
        return user


class TokenSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = ('key',  'user_type')

    def get_user_type(self, obj):
        serializer_data = UserSerializer(
            obj.user
        ).data
        is_participant = serializer_data.get('is_participant')
        is_organizer = serializer_data.get('is_organizer')
        return {
            'is_participant': is_participant,
            'is_organizer': is_organizer
        }


class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'owner')




class EventSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = (
            'id',
            'owner',
            'title',
            'tags',
            'location',
            'num_of_participant',
            'img',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'category',
            'owner',
            'comments', 
            
            )

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta: 
        model = Comment
        fields = ('comment', 'created_date', 'owner', 'event', 'created_time')



class MyEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'




class QrCodeSerializer(serializers.ModelSerializer):
    participant = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = QRCode
        fields = [ 'id',"participant",  "qr_code"]

        read_only_fields = ["qr_code"]





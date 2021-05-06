from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate
from allauth.account.adapter import get_adapter
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from LotDividerAPI import models as apiModels
from rest_auth.serializers import UserDetailsSerializer

# get_user_model() must be used instead of regular
# User model because the custom User model in models.py
# is being used instead of default Django one. This is
# shown in AUTH_USER_MODEL in settings.py
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'alias',
        ]

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:

        model = User
        # these fields are a part of models.User (custom User)
        # model
        fields = [
            'name',
            'alias',
            'email',
            'password',
        ]

    # defining validation function for name
    def validate_name(self, value):
        # check if the name is less than 3 characters
        if len(value) < 3:
            raise serializers.ValidationError(
                "Name must be at least 3 characters!"
            )
        return value
    
    # defining custom validation function on object level. This is
    # to check for the password and password confirmation being the
    # same value
    def validate(self, data):
        # check if the password matches the password confirmation
        if data['password'] != self.initial_data['passwordConfirm']:
            raise serializers.ValidationError(
                "Passwords must match!"
            )
        return data

    # overriding ModelSerializer function
    def get_cleaned_data(self):
        # validated_data represents a dictionary of the data
        # which has been deemed valid by the serializer. The 
        # get function retrieves the value at the requested key, 
        # returning the second argument if the key is not found in
        # the validated_data dictionary
        return {
            'username': self.validated_data.get('username', ''),
            'password': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'alias': self.validated_data.get('alias', '')
        }

    # per django-rest-auth, save function which uses request as 
    # second parameter must be provided. It must also return user
    # object upon completion. Because this is a registration
    # serializer, and because the view only provides the data
    # instead of additional instances to check for already
    # existing objects, the save function will simply create
    # a new record in the database
    def save(self, request):
        user = User.objects.create(
            name=self.validated_data.get('name'),
            alias=self.validated_data.get('alias'),
            email=self.validated_data.get('email'),
            password=make_password(self.validated_data.get('password')),
        )
        return user

class ReadProjectSerializer(serializers.ModelSerializer):
    owners = UserDetailsSerializer()
    class Meta: 
        model = User
        fields = [
            'name',
            'owners'
        ]

class ProjectSerializer(serializers.ModelSerializer):
    owners = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=apiModels.User.objects.all()
    )
    class Meta:
        model = apiModels.Project
        fields = [
            'name',
            'owners',
        ]

    def create(self, validated_data):
        owners = validated_data.pop('owners')
        project = apiModels.Project.objects.create(**validated_data)
        for owner in owners:
            project.owners.add(owner)
        project.save()
        return project

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.ProductType
        fields = [
            'name',
            'fractionalLotsAllowed'
        ]

    # def create(self, validated_data):

class ReadSecuritySerializer(serializers.ModelSerializer):
    productType = ProductTypeSerializer()
    class Meta:
        model = apiModels.Security
        fields = [
            'name',
            'ticker',
            'cusip',
            'productType'
        ]

class SecuritySerializer(serializers.ModelSerializer):
    productType = serializers.PrimaryKeyRelatedField(
        queryset=apiModels.ProductType.objects.all(),
        )
    class Meta:
        model = apiModels.Security
        fields = [
            'name',
            'ticker',
            'cusip',
            'productType',
        ]

    def create(self, validated_data):
        security = apiModels.Security.objects.create(**validated_data)
        return security


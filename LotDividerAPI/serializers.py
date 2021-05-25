from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate
from allauth.account.adapter import get_adapter
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from LotDividerAPI import models as apiModels
from rest_auth.serializers import UserDetailsSerializer
from LotDividerAPI import services, read_serializers
from django.forms.models import model_to_dict


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

class ProjectSerializer(serializers.ModelSerializer):
    owners = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=apiModels.User.objects.all(),
        required=False,
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

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.Portfolio
        fields = [
            'name'
        ]
    
class AccountSerializer(serializers.ModelSerializer):
    portfolio = serializers.PrimaryKeyRelatedField(
        queryset = apiModels.Portfolio.objects.all(),
    )
    class Meta:
        model = apiModels.Account
        fields = [
            'name',
            'portfolio'
        ]
    
class HoldingSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(
        queryset = apiModels.Account.objects.all()
    )
    security = serializers.PrimaryKeyRelatedField(
        queryset = apiModels.Security.objects.all()
    )
    class Meta:
        model = apiModels.Holding
        fields = [
            'account',
            'security'
        ]
        depth = 2

    # def create(self, validated_data):
    #     # securityID = validated_data.pop('security')
    #     # accountID = validated_data.pop('account')
    #     holding = apiModels.Holding.objects.create(
    #         **validated_data
    #     )
    #     return holding
    
class TaxLotSerializer(serializers.ModelSerializer):
    holding = serializers.PrimaryKeyRelatedField(
        queryset = apiModels.Holding.objects.all()
    )
    class Meta:
        model = apiModels.TaxLot
        fields = [
            'number',
            'holding',
            'units',
            'totalFederalCost',
            'totalStateCost',
            'acquisitionDate',
        ]
        depth = 2

class ProposalSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset = apiModels.Project.objects.all()
    )

    class Meta:
        model = apiModels.Proposal
        fields = [
            'name',
            'project',
            'draftPortfolios',
        ]
        depth = 2

class AutoProposalSerializer(serializers.Serializer):
    proposalName = serializers.CharField()
    projectID = serializers.IntegerField()
    accountID = serializers.IntegerField()
    autoCalculate = serializers.BooleanField()
    numberOfPortfolios = serializers.IntegerField()
    targetShares = serializers.DictField(child=serializers.DecimalField(max_digits=8, decimal_places=2))
    method = serializers.ChoiceField(choices=[('HIFO','HIFO')])

    def create(self, validated_data):
        newPortfolio = services.splitPortfolio(
            projectID = validated_data['projectID'],
            accountID = validated_data['accountID'],
            method = validated_data['method'],
            numberOfPortfolios = validated_data['numberOfPortfolios'],
            holdingsDict = validated_data['targetShares'],
        )
        return newPortfolio

    def to_representation(self, instance):
        ppSerializer = read_serializers.ProposalSerializer(instance)
        return {
            'proposal': ppSerializer.data
        }

class DraftPortfolioSerializer(serializers.ModelSerializer):
    proposal = serializers.PrimaryKeyRelatedField(
        queryset = apiModels.Proposal.objects.all()
    )

    class Meta:
        model = apiModels.DraftPortfolio
        fields = [
            'name',
            'proposal',
        ]
        depth = 2

class DraftAccountSerializer(serializers.ModelSerializer):
    draftPortfolio = serializers.PrimaryKeyRelatedField(
        queryset = apiModels.DraftPortfolio.objects.all()
    )

    class Meta:
        model = apiModels.DraftAccount
        fields = [
            'name',
            'draftPortfolio',
        ]
        depth = 2

class DraftHoldingSerializer(serializers.ModelSerializer):
    security = serializers.PrimaryKeyRelatedField(
        queryset = apiModels.Security.objects.all()
    )
    draftAccount = serializers.PrimaryKeyRelatedField(
        queryset = apiModels.DraftAccount.objects.all()
    )

    class Meta:
        model = apiModels.DraftHolding
        fields = [
            'security',
            'draftAccount',
        ]
        depth = 2

class DraftTaxLotSerializer(serializers.ModelSerializer):
    draftHolding = serializers.PrimaryKeyRelatedField(
        queryset = apiModels.DraftHolding.objects.all()
    )
    referencedLot = serializers.PrimaryKeyRelatedField(
        queryset = apiModels.TaxLot.objects.all()
    )

    class Meta:
        model = apiModels.DraftTaxLot
        fields = [
            'draftHolding',
            'units',
            'referencedLot',
        ]
        depth = 2

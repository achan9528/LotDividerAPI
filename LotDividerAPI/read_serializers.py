from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate
from allauth.account.adapter import get_adapter
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from LotDividerAPI import models as apiModels
from rest_auth.serializers import UserDetailsSerializer
from LotDividerAPI import queries
from decimal import Decimal


User = get_user_model()

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.ProductType
        fields = [
            'name',
            'fractionalLotsAllowed'
        ]

class SecuritySerializer(serializers.ModelSerializer):
    productType = ProductTypeSerializer()
    class Meta:
        model = apiModels.Security
        fields = [
            'name',
            'ticker',
            'cusip',
            'productType'
        ]

class DraftTaxLotSerializer(serializers.ModelSerializer):
    marketValue = serializers.SerializerMethodField()

    class Meta:
        model = apiModels.DraftTaxLot
        fields = [
            'id',
            'units',
            'referencedLot',
            'marketValue',
        ]

    def get_marketValue(self, instance):
        closingPrice = queries.getClosingPrice(instance.draftHolding.security.ticker)
        return (Decimal(closingPrice) * instance.units)

class DraftHoldingSerializer(serializers.ModelSerializer):
    draftTaxLots = DraftTaxLotSerializer(many=True)
    security = SecuritySerializer()
    class Meta:
        model = apiModels.DraftHolding
        fields = [
            'id',
            'security',
            'draftTaxLots',
            'draftAccount',
        ]

class DraftAccountSerializer(serializers.ModelSerializer):
    draftHoldings = DraftHoldingSerializer(many=True)
    class Meta:
        model = apiModels.DraftAccount
        fields = [
            'id',
            'name',
            'draftHoldings',
            'draftPortfolio',
        ]
        depth = 2

class DraftPortfolioSerializer(serializers.ModelSerializer):
    draftAccounts = DraftAccountSerializer(many=True)
    class Meta:
        model = apiModels.DraftPortfolio
        fields = [
            'id',
            'name',
            'draftAccounts',
            'proposal',
        ]
        depth = 2


class TaxLotSerializer(serializers.ModelSerializer):
    holding = serializers.StringRelatedField()
    class Meta:
        model = apiModels.TaxLot
        fields = [
            'number',
            'holding',
            'units',
            'totalFederalCost',
            'totalStateCost',
            'acquisitionDate',
            'holding',
        ]

class HoldingSerializer(serializers.ModelSerializer):
    security = SecuritySerializer()
    taxLots = TaxLotSerializer(many=True)
    class Meta:
        model = apiModels.Holding
        fields = [
            'security',
            'account',
            'taxLots',
        ]
    
class AccountSerializer(serializers.ModelSerializer):
    holdings = HoldingSerializer(many=True)
    class Meta:
        model = apiModels.Account
        fields = [
            'id',
            'name',
            'number',
            'holdings',
        ]

class PortfolioSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True)
    class Meta:
        model = apiModels.Portfolio
        fields = [
            'name',
            'accounts',
        ]

class ProposalSerializer(serializers.ModelSerializer):
    draftPortfolios = DraftPortfolioSerializer(many=True)
    holdingsUsed = HoldingSerializer(many=True)
    accountUsed = AccountSerializer()
    class Meta:
        model = apiModels.Proposal
        fields = [
            'id',
            'name',
            'draftPortfolios',
            'project',
            'holdingsUsed',
            'accountUsed',
        ]
        depth = 2

class ProjectSerializer(serializers.ModelSerializer):
    proposals = ProposalSerializer(many=True)
    owners = UserDetailsSerializer(many=True)
    class Meta:
        model = apiModels.Project
        fields = [
            'id',
            'name',
            'proposals',
            'owners'
        ]
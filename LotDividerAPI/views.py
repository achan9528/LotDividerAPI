from LotDividerAPI.models import User
from LotDividerAPI import serializers, read_serializers
from django.http import HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions, mixins, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_auth.registration import views as restAuthViews
from LotDividerAPI import models as apiModels

# Login and Registration views are through the django-rest-auth
# library (see github)

class TestView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'welcome': 'hello!'
        }
        return Response(content)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = apiModels.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.ProjectSerializer
        return serializers.ProjectSerializer

class ProductTypesViewSet(viewsets.ModelViewSet):
    queryset = apiModels.ProductType.objects.all()
    serializer_class = serializers.ProductTypeSerializer

class SecurityViewSet(viewsets.ModelViewSet):
    queryset = apiModels.Security.objects.all()
    serializer_class = serializers.SecuritySerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.SecuritySerializer
        return serializers.SecuritySerializer    
    
class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = apiModels.Portfolio.objects.all()
    serializer_class = serializers.PortfolioSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.PortfolioSerializer
        return serializers.PortfolioSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = apiModels.Account.objects.all()
    serializer_class = serializers.AccountSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.AccountSerializer
        return serializers.AccountSerializer

class HoldingViewSet(viewsets.ModelViewSet):
    queryset = apiModels.Holding.objects.all()
    serializer_class = serializers.HoldingSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.HoldingSerializer
        return serializers.HoldingSerializer

class TaxLotViewSet(viewsets.ModelViewSet):
    queryset = apiModels.TaxLot.objects.all()
    serializer_class = serializers.TaxLotSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.TaxLotSerializer
        return serializers.TaxLotSerializer

class ProposalViewSet(viewsets.ModelViewSet):
    queryset = apiModels.Proposal.objects.all()
    serializer_class = serializers.ProposalSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.ProposalSerializer
        return serializers.ProposalSerializer

class DraftPortfolioViewSet(viewsets.ModelViewSet):
    queryset = apiModels.DraftPortfolio.objects.all()
    serializer_class = serializers.DraftPortfolioSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.DraftPortfolioSerializer
        return serializers.DraftPortfolioSerializer

class DraftAccountViewSet(viewsets.ModelViewSet):
    queryset = apiModels.DraftAccount.objects.all()
    serializer_class = serializers.DraftAccountSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.DraftAccountSerializer
        return serializers.DraftAccountSerializer

class DraftHoldingViewSet(viewsets.ModelViewSet):
    queryset = apiModels.DraftHolding.objects.all()
    serializer_class = serializers.DraftHoldingSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.DraftHoldingSerializer
        return serializers.DraftHoldingSerializer

class DraftTaxLotViewSet(viewsets.ModelViewSet):
    queryset = apiModels.DraftTaxLot.objects.all()
    serializer_class = serializers.DraftTaxLotSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.DraftTaxLotSerializer
        return serializers.DraftTaxLotSerializer
from LotDividerAPI.models import User
from LotDividerAPI import serializers, read_serializers, services
from django.http import HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions, mixins, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_auth.registration import views as restAuthViews
from LotDividerAPI import models as apiModels
from decimal import Decimal
from rest_framework.exceptions import ValidationError
from rest_pandas.views import PandasSimpleView 
from rest_pandas.renderers import PandasExcelRenderer

# Login and Registration views are through the django-rest-auth
# library (see github)

class TestView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        content = {
            'welcome': 'hello!'
        }
        return Response(content)

class GetGenericUserInfo(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        print(user.name)
        content = {
            'username': user.name
        }
        return Response(content)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = apiModels.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classses = [JSONRenderer]
    parser_classes = [JSONParser]
    
    def get_queryset(self):
        if self.request.query_params.get('userSpecific'):
            user = self.request.user
            return apiModels.User.objects.get(id=user.id).projects.all()
        return apiModels.Project.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.ProjectSerializer
        return serializers.ProjectSerializer

    def create(self, request, *args, **kwargs):
        print(self.request.user.id)
        project_owners = request.data['owners']
        project_owners.append(self.request.user.id)
        request.data['owners'] = project_owners
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = apiModels.ProductType.objects.all()
    serializer_class = serializers.ProductTypeSerializer
    renderer_classses = [JSONRenderer]
    parser_classes = [JSONParser]

class SecurityViewSet(viewsets.ModelViewSet):
    queryset = apiModels.Security.objects.all()
    serializer_class = serializers.SecuritySerializer
    renderer_classses = [JSONRenderer]
    parser_classes = [JSONParser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.SecuritySerializer
        return serializers.SecuritySerializer    
    
class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = apiModels.Portfolio.objects.all()
    serializer_class = serializers.PortfolioSerializer
    renderer_classses = [JSONRenderer]
    parser_classes = [MultiPartParser, JSONParser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.PortfolioSerializer
        return serializers.PortfolioSerializer

    def create(self, request, *args, **kwargs):
        # pass request to the parsing service
        # if successful, return Success Response,
        # else return Error
        portfolio = services.processNewPortfolio(request)
        serializer = read_serializers.PortfolioSerializer
        serializer = serializer(portfolio)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AccountViewSet(viewsets.ModelViewSet):
    queryset = apiModels.Account.objects.all()
    serializer_class = serializers.AccountSerializer
    renderer_classses = [JSONRenderer]
    parser_classes = [JSONParser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.AccountSerializer
        return serializers.AccountSerializer

class HoldingViewSet(viewsets.ModelViewSet):
    queryset = apiModels.Holding.objects.all()
    serializer_class = serializers.HoldingSerializer
    renderer_classses = [JSONRenderer]
    parser_classes = [JSONParser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.HoldingSerializer
        return serializers.HoldingSerializer

class TaxLotViewSet(viewsets.ModelViewSet):
    queryset = apiModels.TaxLot.objects.all()
    serializer_class = serializers.TaxLotSerializer
    renderer_classses = [JSONRenderer]
    parser_classes = [JSONParser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.TaxLotSerializer
        return serializers.TaxLotSerializer

class ProposalViewSet(viewsets.ModelViewSet):
    queryset = apiModels.Proposal.objects.all()
    serializer_class = serializers.ProposalSerializer
    renderer_classses = [JSONRenderer]
    parser_classes = [JSONParser]

    def get_serializer_class(self):
        print(self.request.data)
        if self.request.method == 'GET':
            return read_serializers.ProposalSerializer
        if self.request.method == 'POST' and self.request.data['autoCalculate'] == 'true':
            return serializers.AutoProposalSerializer
        return serializers.ProposalSerializer

class DraftPortfolioViewSet(viewsets.ModelViewSet):
    queryset = apiModels.DraftPortfolio.objects.all()
    serializer_class = serializers.DraftPortfolioSerializer
    renderer_classses = [JSONRenderer]
    parser_classes = [JSONParser]    

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.DraftPortfolioSerializer
        return serializers.DraftPortfolioSerializer

class DraftAccountViewSet(viewsets.ModelViewSet):
    queryset = apiModels.DraftAccount.objects.all()
    serializer_class = serializers.DraftAccountSerializer
    renderer_classses = [JSONRenderer]
    parser_classes = [JSONParser]    

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.DraftAccountSerializer
        return serializers.DraftAccountSerializer

class DraftHoldingViewSet(viewsets.ModelViewSet):
    queryset = apiModels.DraftHolding.objects.all()
    serializer_class = serializers.DraftHoldingSerializer
    renderer_classses = [JSONRenderer]
    parser_classes = [JSONParser]    

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.DraftHoldingSerializer
        return serializers.DraftHoldingSerializer

class DraftTaxLotViewSet(viewsets.ModelViewSet):
    queryset = apiModels.DraftTaxLot.objects.all()
    serializer_class = serializers.DraftTaxLotSerializer
    renderer_classses = [JSONRenderer]
    parser_classes = [JSONParser]    

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return read_serializers.DraftTaxLotSerializer
        return serializers.DraftTaxLotSerializer

class DraftTaxLotBatchUpdate(APIView):
    parser_classes = [JSONParser]
    def patch(self, request, *args, **kwargs):
        data = request.data
        instances = []
        print(data)
        for productType, productTypeDict in data.items():
            print(productType)
            for ticker, tickerDict in productTypeDict.items():
                for lots, lotDict in tickerDict.items():
                    for account, accountDict in lotDict.items():
                        try:
                            print('test')
                            print(accountDict)
                            instance = apiModels.DraftTaxLot.objects.get(id=int(accountDict['draftTaxLotID']))
                            instance.units = Decimal(float(accountDict['units']))
                            instance.save()
                            instances.append(instance)
                        except (apiModels.DraftTaxLot.DoesNotExist, ValueError):
                            raise ValidationError()
        serializer = read_serializers.DraftTaxLotSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DownloadProposal(PandasSimpleView):
    renderer_classes = [PandasExcelRenderer]

    def update_pandas_headers(self, response):
        headers = self.get_pandas_headers(self.request)
        for key, val in headers.items():
            response[key] = val
        return response

    def get_pandas_filename(self, request, format):
        return request.query_params.get('fileName')

    def get_data(self,request,*args,**kwargs):
        print(request)
        print(kwargs)
        return services.exportProposal(kwargs.get('proposalID'),**request.query_params)

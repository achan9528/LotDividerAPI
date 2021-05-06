from LotDividerAPI.models import User
from LotDividerAPI import serializers
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
            return serializers.ReadProjectSerializer
        return serializers.ProjectSerializer

class ProductTypesViewSet(viewsets.ModelViewSet):
    queryset = apiModels.ProductType.objects.all()
    serializer_class = serializers.ProductTypeSerializer

class SecurityViewSet(viewsets.ModelViewSet):
    queryset = apiModels.Security.objects.all()
    serializer_class = serializers.SecuritySerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ReadSecuritySerializer
        return serializers.SecuritySerializer    
    


from django.urls import path, include
from LotDividerAPI import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'securities', views.SecurityViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'products', views.ProductTypesViewSet)

urlpatterns = [
    path('api/welcome/', views.TestView.as_view()),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/', include(router.urls)),
]
from django.urls import path, re_path, include
from LotDividerAPI import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'securities', views.SecurityViewSet)
router.register(r'product-types', views.ProductTypeViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'portfolios', views.PortfolioViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'holdings', views.HoldingViewSet)
router.register(r'tax-lots', views.TaxLotViewSet)
router.register(r'proposals', views.ProposalViewSet)
router.register(r'draft-portfolios', views.DraftPortfolioViewSet)
router.register(r'draft-accounts', views.DraftAccountViewSet)
router.register(r'draft-holdings', views.DraftHoldingViewSet)
router.register(r'draft-taxlots', views.DraftTaxLotViewSet)

urlpatterns = [
    path('api/welcome/', views.TestView.as_view()),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/draft-taxlots/batch/', views.DraftTaxLotBatchUpdate.as_view()),
    re_path(r'^api/proposals/(?P<proposalID>[0-9]{1,})/download/$', views.DownloadProposal.as_view()),
    path('api/get-user-info/', views.GetGenericUserInfo.as_view()),
    path('api/', include(router.urls)),
]
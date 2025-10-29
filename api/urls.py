from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'scammers', views.ScammerViewSet, basename='scammer')
router.register(r'scammernames', views.ScammerNameViewSet)
router.register(r'scammerphonenumbers', views.ScammerPhoneNumberViewSet)
router.register(r'scammeremails', views.ScammerEmailViewSet)
router.register(r'scammerwebsites', views.ScammerWebsiteViewSet)
router.register(r'scammerimages', views.ScammerImageViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'scammerpaymentaccounts', views.ScammerPaymentAccountViewSet)
router.register(r'scammerprofiles', views.ScammerProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', views.SearchView.as_view(), name='scammer-search'),
]

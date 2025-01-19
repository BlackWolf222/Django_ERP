from django.urls import path, include
from djangoapp.views import CompanyViewSet, EmployeeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path, include
from djangoapp.views import CompanyViewSet, EmployeeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'company', CompanyViewSet, basename='list')
router.register(r'employees', EmployeeViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
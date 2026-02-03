from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecursoViewSet

router = DefaultRouter()
router.register(r'recursos', RecursoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
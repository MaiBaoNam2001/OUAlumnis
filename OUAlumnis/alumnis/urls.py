from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('alumni-profiles', views.AlumniProfileViewSet, basename='alumni-profiles')

urlpatterns = [
    path('', include(router.urls)),
]

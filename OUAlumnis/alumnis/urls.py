from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('alumni-profiles', views.AlumniProfileViewSet, basename='alumni-profiles')

urlpatterns = [
    path('', include(router.urls)),
]

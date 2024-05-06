from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('genders', views.GenderViewSet, basename='genders')
router.register('faculties', views.FacultyViewSet, basename='faculties')
router.register('school-years', views.SchoolYearViewSet, basename='school-years')
router.register('users', views.UserViewSet, basename='users')
router.register('alumni-profiles', views.AlumniProfileViewSet, basename='alumni-profiles')

urlpatterns = [
    path('', include(router.urls)),
]

import json
import traceback

from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from . import models, serializers


class UserViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = models.User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.action in ['current_user']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['GET'], detail=False, url_path='current-user')
    def current_user(self, request):
        user = request.user
        if user.role.code.__eq__('ALUMNI'):
            alumni_profile = models.AlumniProfile.objects.get(user=user)
            return Response(serializers.AlumniProfileSerializer(alumni_profile, context={'request': request}).data)
        elif user.role.code.__eq__('LECTURER'):
            lecturer_profile = models.LecturerProfile.objects.get(user=user)
            if user.is_password_expired():
                user.is_active = False
                user.save()

                lecturer_profile.is_locked = True
                lecturer_profile.save()

                return Response({'error': 'User account locked'}, status=status.HTTP_423_LOCKED)
            return Response(serializers.LecturerProfileSerializer(lecturer_profile, context={'request': request}).data)
        return Response(serializers.UserSerializer(user).data)


class AlumniProfileViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = models.AlumniProfile.objects.filter(user__is_active=True)
    serializer_class = serializers.AlumniProfileSerializer

    @action(methods=['POST'], detail=False, url_path='register')
    def register(self, request):
        try:
            user_data = json.loads(request.data['user'])
            alumni_profile_data = request.data.copy()
            del alumni_profile_data['user']

            user = models.User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.date_of_birth = user_data['date_of_birth']
            user.gender = models.Gender.objects.get(code=user_data['gender'])
            user.avatar = user_data['avatar']
            user.cover_image = user_data['cover_image']
            user.role = models.Role.objects.get(code='ALUMNI')
            user.is_active = False
            user.save()

            alumni_profile = models.AlumniProfile.objects.create(
                user=user,
                student_id=alumni_profile_data['student_id'],
                image=alumni_profile_data['image'],
                faculty=models.Faculty.objects.get(code=alumni_profile_data['faculty']),
                major=models.Major.objects.get(code=alumni_profile_data['major']),
                school_year=models.SchoolYear.objects.get(code=alumni_profile_data['school_year']),
                workplace=alumni_profile_data['workplace'],
                position=alumni_profile_data['position'],
                bio=alumni_profile_data['bio']
            )

            serializer = serializers.AlumniProfileSerializer(alumni_profile, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ValidationError, KeyError) as e:
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

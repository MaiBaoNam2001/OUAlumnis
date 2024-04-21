from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(source='avatar')
    cover_image = serializers.SerializerMethodField(source='cover_image')

    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'date_of_birth', 'gender', 'avatar',
                  'cover_image', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True}
        }

    def get_avatar(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            return request.build_absolute_uri('/static/%s' % obj.avatar.name) if request else ''

    def get_cover_image(self, obj):
        if obj.cover_image:
            request = self.context.get('request')
            return request.build_absolute_uri('/static/%s' % obj.cover_image.name) if request else ''


class AlumniProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    image = serializers.SerializerMethodField(source='image')

    class Meta:
        model = models.AlumniProfile
        fields = ['user', 'student_id', 'image', 'faculty', 'major', 'school_year', 'workplace', 'position', 'bio']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri('/static/%s' % obj.image.name) if request else ''


class LecturerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    image = serializers.SerializerMethodField(source='image')

    class Meta:
        model = models.LecturerProfile
        fields = ['user', 'image', 'faculty', 'academic_rank', 'academic_degree', 'bio']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri('/static/%s' % obj.image.name) if request else ''

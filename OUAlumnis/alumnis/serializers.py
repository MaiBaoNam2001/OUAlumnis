from rest_framework import serializers
from . import models


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gender
        fields = ['code', 'name']


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Faculty
        fields = ['code', 'name']


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Major
        fields = ['code', 'name', 'faculty']


class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchoolYear
        fields = ['code', 'name']


class AcademicRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AcademicRank
        fields = ['code', 'name']


class AcademicDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AcademicDegree
        fields = ['code', 'name']


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


class UserGetSerializer(UserSerializer):
    gender = GenderSerializer()

    class Meta:
        model = UserSerializer.Meta.model
        fields = UserSerializer.Meta.fields
        extra_kwargs = UserSerializer.Meta.extra_kwargs


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


class AlumniProfileGetSerializer(AlumniProfileSerializer):
    user = UserGetSerializer()
    faculty = FacultySerializer()
    major = MajorSerializer()
    school_year = SchoolYearSerializer()

    class Meta:
        model = AlumniProfileSerializer.Meta.model
        fields = AlumniProfileSerializer.Meta.fields


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


class LecturerProfileGetSerializer(LecturerProfileSerializer):
    user = UserGetSerializer()
    faculty = FacultySerializer()
    academic_rank = AcademicRankSerializer()
    academic_degree = AcademicDegreeSerializer()

    class Meta:
        model = LecturerProfileSerializer.Meta.model
        fields = LecturerProfileSerializer.Meta.fields

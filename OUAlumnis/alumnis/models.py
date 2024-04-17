from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Gender(BaseModel):
    code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Role(BaseModel):
    code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Faculty(BaseModel):
    code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Major(BaseModel):
    code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SchoolYear(BaseModel):
    code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class AcademicRank(BaseModel):
    code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class AcademicDegree(BaseModel):
    code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m', blank=True, null=True)
    cover_image = models.ImageField(upload_to='cover_images/%Y/%m', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)


class AlumniProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_id = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='images/%Y/%m')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    workplace = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)

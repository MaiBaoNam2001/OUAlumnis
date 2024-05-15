from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True)
    date_of_birth = models.DateField(null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m', blank=True, null=True)
    cover_image = models.ImageField(upload_to='cover_images/%Y/%m', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    password_reset_expiry = models.DateTimeField(blank=True, null=True)

    def is_password_expired(self):
        if self.password_reset_expiry is None:
            return False
        return timezone.now() >= self.password_reset_expiry


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
    is_confirmed = models.BooleanField(default=True)


class LecturerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to='images/%Y/%m')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    academic_rank = models.ForeignKey(AcademicRank, on_delete=models.CASCADE)
    academic_degree = models.ForeignKey(AcademicDegree, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    is_locked = models.BooleanField(default=False)


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    is_comment_locked = models.BooleanField(default=False)


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content


class InteractionType(BaseModel):
    code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    icon = models.FileField(upload_to='icons', validators=[FileExtensionValidator(['svg'])], unique=True)

    def __str__(self):
        return self.name


class Interaction(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interaction_type = models.ForeignKey(InteractionType, on_delete=models.CASCADE)
    is_interacted = models.BooleanField(default=True)

    def __str__(self):
        return self.is_interacted

    class Meta:
        unique_together = ('post', 'user')


class NotificationType(BaseModel):
    code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Notification(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.content

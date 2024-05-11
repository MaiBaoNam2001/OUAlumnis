from django import forms
from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.safestring import mark_safe

from . import models


class GenderAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active']
    list_filter = ['code', 'name']
    search_fields = ['name']


class RoleAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active']
    list_filter = ['code', 'name']
    search_fields = ['name']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.exclude(code='ADMIN')


class FacultyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active']
    list_filter = ['code', 'name']
    search_fields = ['name']


class MajorAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'faculty', 'is_active']
    list_filter = ['code', 'name', 'faculty']
    search_fields = ['name']


class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active']
    list_filter = ['code', 'name']
    search_fields = ['name']


class AcademicRankAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active']
    list_filter = ['code', 'name']
    search_fields = ['name']


class AcademicDegreeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active']
    list_filter = ['code', 'name']
    search_fields = ['name']


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = models.Role.objects.exclude(code='ADMIN')


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'username', 'email', 'role', 'is_active']
    list_filter = ['id', 'username', 'email', 'role']
    search_fields = ['first_name', 'last_name', 'username', 'email']
    exclude = ['password', 'is_superuser', 'is_staff', 'is_active']
    readonly_fields = ['avt', 'cover_img']
    form = UserForm

    def avt(self, obj):
        return mark_safe('<img src="/static/{url}" width="120" />'.format(url=obj.avatar.name)) if obj.avatar else ''

    def cover_img(self, obj):
        return mark_safe(
            '<img src="/static/{url}" width="120" />'.format(url=obj.cover_image.name)) if obj.cover_image else ''

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.exclude(id=1)


class AlumniProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = models.User.objects.filter(role__code='ALUMNI')


class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'faculty', 'major', 'school_year', 'is_confirmed']
    list_filter = ['user', 'student_id', 'faculty', 'major', 'school_year']
    search_fields = ['student_id']
    exclude = ['is_confirmed']
    readonly_fields = ['img']
    actions = [
        'accept_selected_alumni_profiles_and_send_notification_mail',
        'reject_selected_alumni_profiles_and_send_notification_mail'
    ]
    form = AlumniProfileForm

    def img(self, obj):
        return mark_safe('<img src="/static/{url}" width="120" />'.format(url=obj.image.name)) if obj.image else ''

    def accept_selected_alumni_profiles_and_send_notification_mail(self, request, queryset):
        for alumni_profile in queryset:
            user = alumni_profile.user
            if not alumni_profile.is_confirmed:
                alumni_profile.is_confirmed = True
                alumni_profile.save()

                subject = 'Xác nhận tài khoản cựu sinh viên'
                body = f"""
                    Xin chào {user.last_name} {user.first_name},

                    Bạn đã được xác nhận là cựu sinh viên của trường. Vui lòng mở ứng dụng OUAlumnis để tiến hành đăng nhập.

                    Trân trọng,

                    Ban quản trị OUAlumnis
                    """
                send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email])

    def reject_selected_alumni_profiles_and_send_notification_mail(self, request, queryset):
        for alumni_profile in queryset:
            user = alumni_profile.user
            if not alumni_profile.is_confirmed:
                subject = 'Từ chối xác nhận tài khoản cựu sinh viên'
                body = f"""
                    Xin chào {user.last_name} {user.first_name},

                    Rất tiếc, chúng tôi không thể xác nhận tài khoản cựu sinh viên của bạn.

                    Lý do: Thông tin bạn cung cấp không chính xác

                    Bạn có thể thử đăng ký lại sau.

                    Trân trọng,

                    Ban quản trị OUAlumnis
                    """
                send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email])
                user.delete()


class LecturerProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = models.User.objects.filter(role__code='LECTURER')


class LecturerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'faculty', 'academic_rank', 'academic_degree', 'is_locked']
    list_filter = ['user', 'faculty', 'academic_rank', 'academic_degree']
    exclude = ['is_locked']
    readonly_fields = ['img']
    actions = [
        'unclock_selected_lecturer_profiles_and_send_notification_mail'
    ]
    form = LecturerProfileForm

    def img(self, obj):
        return mark_safe('<img src="/static/{url}" width="120" />'.format(url=obj.image.name)) if obj.image else ''

    def unclock_selected_lecturer_profiles_and_send_notification_mail(self, request, queryset):
        for lecturer_profile in queryset:
            user = lecturer_profile.user
            if lecturer_profile.is_locked:
                lecturer_profile.is_locked = False
                lecturer_profile.save()

                user.password_reset_expiry = timezone.now() + timezone.timedelta(days=1)
                user.save()

                subject = 'Mở khóa tài khoản giảng viên'
                body = f"""
                    Kính gửi {user.last_name} {user.first_name},

                    Chúng tôi đã mở khóa tài khoản giảng viên của bạn. Vui lòng đổi mật khẩu trong vòng 24 giờ nếu không tài khoản sẽ bị khóa trở lại.
                    
                    Trân trọng,

                    Ban quản trị OUAlumnis
                    """
                send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email])


admin.site.register(models.Gender, GenderAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.Faculty, FacultyAdmin)
admin.site.register(models.Major, MajorAdmin)
admin.site.register(models.SchoolYear, SchoolYearAdmin)
admin.site.register(models.AcademicRank, AcademicRankAdmin)
admin.site.register(models.AcademicDegree, AcademicDegreeAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.AlumniProfile, AlumniProfileAdmin)
admin.site.register(models.LecturerProfile, LecturerProfileAdmin)

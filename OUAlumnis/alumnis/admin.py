from django import forms
from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
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
        queryset = super(RoleAdmin, self).get_queryset(request)
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
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['role'].queryset = models.Role.objects.exclude(code='ADMIN')


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'username', 'email', 'role', 'is_active']
    list_filter = ['id', 'username', 'email', 'role']
    search_fields = ['first_name', 'last_name', 'username', 'email']
    exclude = ['is_superuser', 'is_staff', 'is_active']
    form = UserForm

    def get_queryset(self, request):
        queryset = super(UserAdmin, self).get_queryset(request)
        return queryset.exclude(id=1)


class AlumniProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlumniProfileForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = models.User.objects.exclude(id=1)


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
            if not alumni_profile.is_confirmed and not user.is_active:
                user.is_active = True
                user.save()

                alumni_profile.is_confirmed = True
                alumni_profile.save()

                login_url = ''  # Note
                subject = 'Xác nhận tài khoản cựu sinh viên'
                body = f"""
                    Xin chào {user.last_name} {user.first_name},

                    Bạn đã được xác nhận là cựu sinh viên của trường. Vui lòng nhấp vào liên kết sau để tiến hành đăng nhập:

                    {login_url}

                    Trân trọng,

                    Ban quản trị OUAlumnis
                    """
                send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email])

    def reject_selected_alumni_profiles_and_send_notification_mail(self, request, queryset):
        for alumni_profile in queryset:
            user = alumni_profile.user
            if not alumni_profile.is_confirmed and not user.is_active:
                subject = 'Từ chối xác nhận tài khoản cựu sinh viên'
                body = f"""
                    Xin chào {user.last_name} {user.first_name},

                    Rất tiếc, chúng tôi không thể xác nhận tài khoản cựu sinh viên của bạn.

                    Lý do: Thông tin bạn cung cấp không đúng
                    
                    Bạn có thể thử đăng ký lại sau.

                    Trân trọng,

                    Ban quản trị OUAlumnis
                    """
                send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email])
                user.delete()


admin.site.register(models.Gender, GenderAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.Faculty, FacultyAdmin)
admin.site.register(models.Major, MajorAdmin)
admin.site.register(models.SchoolYear, SchoolYearAdmin)
admin.site.register(models.AcademicRank, AcademicRankAdmin)
admin.site.register(models.AcademicDegree, AcademicDegreeAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.AlumniProfile, AlumniProfileAdmin)

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone

from . import models


@receiver(post_save, sender=models.User)
def set_default_password_for_user_admin_site(sender, instance, created, **kwargs):
    if created:
        if not instance.password:
            instance.set_password('ou@123')
            instance.save()


@receiver(post_save, sender=models.LecturerProfile)
def set_password_reset_expiry(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        if user.password_reset_expiry is None:
            user.password_reset_expiry = timezone.now() + timezone.timedelta(days=1)
            user.save()

            subject = 'Thông tin tài khoản giảng viên'
            body = f"""
                    Kính gửi {user.last_name} {user.first_name},

                    Chúng tôi rất vui mừng thông báo rằng bạn đã được cấp tài khoản giảng viên trên hệ thống mạng xã hội cựu sinh viên OUAlumnis.

                    Thông tin tài khoản của bạn:
                    - Tên đăng nhập: {user.username}
                    - Mật khẩu: ou@123
                    
                    Lưu ý:
                    - Vui lòng đổi mật khẩu trong vòng 24 giờ nếu không tài khoản sẽ bị khóa.
                    - Nếu tài khoản của bạn bị khóa, vui lòng liên hệ với chúng tôi để được hỗ trợ mở khóa tài khoản.

                    Trân trọng,

                    Ban quản trị OUAlumnis
                    """
            send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email])


@receiver(pre_save, sender=models.AlumniProfile)
def delete_alumni_profile_old_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = models.AlumniProfile.objects.get(user=instance.user).image
        except models.AlumniProfile.DoesNotExist:
            old_image = None

        if old_image and old_image.name != instance.image.name:
            old_image.delete(save=False)


@receiver(pre_delete, sender=models.AlumniProfile)
def delete_alumni_profile_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete()


@receiver(pre_save, sender=models.LecturerProfile)
def delete_lecturer_profile_old_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = models.LecturerProfile.objects.get(user=instance.user).image
        except models.LecturerProfile.DoesNotExist:
            old_image = None

        if old_image and old_image.name != instance.image.name:
            old_image.delete(save=False)


@receiver(pre_delete, sender=models.LecturerProfile)
def delete_lecturer_profile_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete()


@receiver(pre_save, sender=models.User)
def delete_user_old_avatar(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_avatar = models.User.objects.get(pk=instance.pk).avatar
        except models.User.DoesNotExist:
            old_avatar = None

        if old_avatar and old_avatar.name != instance.avatar.name:
            old_avatar.delete(save=False)


@receiver(pre_save, sender=models.User)
def delete_user_old_cover_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_cover_image = models.User.objects.get(pk=instance.pk).cover_image
        except models.User.DoesNotExist:
            old_cover_image = None

        if old_cover_image and old_cover_image.name != instance.cover_image.name:
            old_cover_image.delete(save=False)


@receiver(pre_delete, sender=models.User)
def delete_user_avatar(sender, instance, **kwargs):
    if instance.avatar:
        instance.avatar.delete()


@receiver(pre_delete, sender=models.User)
def delete_user_cover_image(sender, instance, **kwargs):
    if instance.cover_image:
        instance.cover_image.delete()

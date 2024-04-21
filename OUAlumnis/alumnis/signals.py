from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from . import models


@receiver(post_save, sender=models.User)
def set_default_password_for_user_admin_site(sender, instance, created, **kwargs):
    if created:
        if not instance.password:
            instance.set_password('ou@123')
            instance.save()


@receiver(post_save, sender=models.AlumniProfile)
def confirm_if_user_is_active(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        if user.is_active:
            instance.is_confirmed = True
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

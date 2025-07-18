from core.models.basemodel import SafeBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models.user import User

class OTP(SafeBaseModel):
    phone_number = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'OTP'
        verbose_name_plural = "OTPs"

    def __str__(self):
        return f"OTP for {self.phone_number}"
    

class UserSMS(SafeBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sms_messages', blank=True, null=True)
    text = models.TextField()
    is_sent = models.BooleanField(default=False)
    category = models.CharField(max_length=50, choices=[
        ('info', _('Information')),
        ('password', _('Password')),
        ('reminder', _('Reminder')),
    ])

    def __str__(self):
        return f"Sent: {self.is_sent}"
    
    class Meta:
        verbose_name = 'User SMS'
        verbose_name_plural = 'User SMS'
        ordering = ['-created_datetime']
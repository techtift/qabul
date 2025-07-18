from core.models.basemodel import SafeBaseModel
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _


class User(SafeBaseModel):
    phone_number = models.CharField(max_length=15, unique=True,null=True,blank=True)
    password = models.CharField(max_length=128)
    source = models.CharField(max_length=50, default="web", null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    LANG_CHOICES = (
        ('en', 'English'),
        ('ru', 'Russian'),
        ('uz', 'Uzbek')
    )
    tg_id = models.BigIntegerField(null=True, blank=True,unique=True)
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, null=True, blank=True)
    registered_by_bot=models.BooleanField(default=False)

    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return f"User {self.phone_number} - Verified: {self.is_verified}"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"
        ordering = ['-created_datetime']
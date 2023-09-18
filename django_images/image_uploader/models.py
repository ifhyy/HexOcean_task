from django.contrib.auth import get_user_model
from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class AccountTier(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Tier')
    thumbnail_sizes = models.CharField(
        max_length=30,
        validators=[validate_comma_separated_integer_list],
        verbose_name='thumbnail height in px')
    originally_uploaded_image = models.BooleanField(
        default=False,
        verbose_name='Send link to the originally uploaded image')
    generate_exp_links = models.BooleanField(
        default=False,
        verbose_name='Ability to generate expiring links')

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    account_tier = models.ForeignKey(
        AccountTier,
        on_delete=models.PROTECT,
        related_name='accounts',
        default=None,
        null=True
    )

    def __str__(self):
        return self.username


class Image(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='images/', default=None)

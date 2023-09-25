from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Customer(User):
    avatar = models.ImageField(
        verbose_name='аватар',
        blank=True)
    is_subscriber = models.BooleanField(
        verbose_name='подписчик',
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата обновления'
    )

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

    def __str__(self):
        return self.username

from django.db import models


# Create your models here.
class ClientsModel(models.Model):
    username = models.CharField(
        max_length=52,
        blank=True,
        null=True
    )
    user_id = models.PositiveIntegerField(
        unique=True
    )
    active = models.BooleanField(
        default=True
    )
    id_doctor = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return f'{self.username}{self.user_id}'


class Messages(models.Model):
    data_created = models.DateTimeField(
        auto_now_add=True
    )
    user_id = models.ForeignKey(
        'ClientsModel',
        on_delete=models.CASCADE,
        related_name='message_user_id'
    )
    message = models.CharField(
        max_length=1024
    )
    finished = models.BooleanField(
        default=False
    )
    maker_id = models.ForeignKey(
        'ClientsModel',
        on_delete=models.CASCADE,
        related_name='message_maker_id',
        blank=True,
        null=True
    )
    time_to_exit = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    active = models.BooleanField(
        default=True
    )
    rating = models.CharField(
        default='0',
        max_length=100
    )

    class Meta:
        verbose_name = 'Messages'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.message

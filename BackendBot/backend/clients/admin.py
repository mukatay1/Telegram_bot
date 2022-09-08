from django.contrib import admin
from .models import ClientsModel, Messages


# Register your models here.
@admin.register(ClientsModel)
class ClientsAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'user_id',
        'active',
        'id_doctor'
    )


@admin.register(Messages)
class ClientsAdmin(admin.ModelAdmin):
    list_display = (
        'data_created',
        'user_id',
        'maker_id',
        'message',
        'finished',
        'active',
        'time_to_exit',
        'rating'
    )

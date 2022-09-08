from rest_framework import serializers
from .models import (ClientsModel,
                     Messages
                     )


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientsModel
        fields = '__all__'


class MessagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'

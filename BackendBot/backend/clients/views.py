from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .serializers import (ClientSerializer,
                          MessagesSerializers
                          )

from .models import (ClientsModel,
                     Messages
                     )


class ClientsView(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active', 'id_doctor', 'user_id']
    serializer_class = ClientSerializer
    queryset = ClientsModel.objects.all()


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    queryset = ClientsModel.objects.all()


class MessagesView(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['finished', 'active', 'user_id', 'message', 'maker_id']
    serializer_class = MessagesSerializers
    queryset = Messages.objects.all()


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessagesSerializers
    queryset = Messages.objects.all()

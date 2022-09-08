from django.urls import path

from .views import (ClientsView,
                    MessagesView,
                    ClientDetailView,
                    MessageDetailView,
                    )

urlpatterns = [
    path('clients/', ClientsView.as_view(), name='clients'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='clients-detail'),
    path('messages/', MessagesView.as_view(), name='messages'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='messages-detail')
]

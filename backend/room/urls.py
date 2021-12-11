from django.urls import path

from .views import RoomView, SingleRoomView

urlpatterns = [
    # api url
    path('room/', RoomView.as_view()),
    path('room/<int:pk>/', SingleRoomView.as_view()),
]

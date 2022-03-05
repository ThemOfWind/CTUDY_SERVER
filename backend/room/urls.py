from django.urls import path

from .views import RoomView, SingleRoomView, RoomMemberView, MemberListView

urlpatterns = [
    # api url
    path('room/', RoomView.as_view()),
    path('room/<int:pk>/', SingleRoomView.as_view()),
    path('room-member/<int:pk>/', RoomMemberView.as_view()),
    path('member/', MemberListView.as_view()),
]

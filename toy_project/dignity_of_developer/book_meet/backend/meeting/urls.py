from django.urls import path
from . import views

app_name = "meeting"  # URL Reverse에서 namespace역할을 하게 됨

urlpatterns = [
    path("rooms/", views.MeetingCreate.as_view(), name="meeting_rooms"),
]

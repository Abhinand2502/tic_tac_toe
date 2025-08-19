from django.contrib import admin
from django.urls import path
from game import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("game/<str:room_name>/", views.room, name="room"),

]

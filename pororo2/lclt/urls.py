from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'lclt'

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='lclt/login.html'),name='login'),
    path('', views.index , name='index'),
    path('signup/',views.signup,name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('myuser/<str:user_id>/',views.myuser, name="myuser"),
    path('room-make/',views.room_make, name="room_make"),
    path('room/<str:code_id>/',views.roomcam, name="room"),
    path('room-modify/<str:code_id>/',views.room_modify, name="room_modify"),
    path('room-delete/<str:code_id>/', views.delete_room, name='delete_room'),
    path('allroom/',views.allroom,name="allroom"),
    path('notice/',views.notice,name="notice"),
    path('notice-detail/<int:notice_id>/',views.notice_detail,name="notice-detail")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerUser,name='register'),
    path('',views.home,name="home"),
    path('profile/<str:pk>',views.userProfile,name='user-profile'),
    path('account/',views.userAccount,name='account'),
    path('edit-account/',views.editAccount,name='edit-account'),
    path('timetable/',views.timetable,name='timetable'),
    path('recording/',views.recording,name='recording'),
    path("emotion_analysis/", views.emotion_analysis, name="emotion_analysis"),
    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('get_emotion_data/<int:lecture_id>/', views.get_emotion_data, name='get_emotion_data'),
    
]



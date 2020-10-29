from django.urls import path
from . import views


app_name = "Core"
urlpatterns = [
    path('manager/login/', views.LoginView.as_view(), name='login'),
    path('manager/register/', views.RegisterView, name='register'),
    path('manager/dashboard/',views.DashboardView.as_view(), name='dashboard'),
    path('', views.WelcomeClass.as_view(), name="Welcome"),
    path('detect_webbycamera/', views.DetectCamera.as_view(), name="detect_webbycamera"),
    path('postajax/', views.postFriend, name = "post_friend"),
    path('chonbienso/', views.chonbienso.as_view(), name="chonbienso"),
    path('nhandienHinhAnh/', views.nhandienHinhAnh, name = "nhandienHinhAnh"),
    path('nhandien/', views.NhanDienView.as_view(), name = 'nhandien'),
]


from django.urls import path
from . import views

urlpatterns = [
	path('register', views.ProfileRegister.as_view(), name='register'),
	path('login', views.ProfileLogin.as_view(), name='login'),
	path('logout', views.ProfileLogout.as_view(), name='logout'),
	path('profile', views.ProfileView.as_view(), name='profile'),
	path('delete', views.ProfileDelete.as_view(), name='delete'),
	path('update', views.ProfileUpdate.as_view(), name='update')
]
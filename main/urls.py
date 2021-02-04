from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('entries', views.edit_entries, name='entries'),

    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),

    path('logout', views.logout_user, name='logout'),
    path('profile/change-password', views.change_password, name='change_password')

]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginpage, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_task/<int:id>/', views.delete_task, name='delete_task'),
]

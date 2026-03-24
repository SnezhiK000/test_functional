from django.contrib import admin
from django.urls import path
from testing import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register_view, name='register_view'),
    path('student/', views.show_students, name='show_students'),
    path('student/create/', views.show_create, name='show_create'),
    path('student/edit/<int:id>/', views.show_edit, name='show_edit'),
    path('student/delete/<int:id>/', views.show_delete, name='show_delete'),
]
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('projects/', views.projects, name='projects'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('tasks/', views.tasks, name='tasks'),
    path('profile/', views.profile_view, name='profile'),
    path('task/accept/<int:task_id>/', views.accept_task, name='accept_task'),
    path('task/status/<int:task_id>/<str:status>/', views.change_task_status, name='change_task_status'),
]
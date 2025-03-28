from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    LoginView,
    LogoutView,
    HomeView,
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path(
        'projects/<int:pk>/', ProjectDetailView.as_view(),
        name='project_detail'),
    path('projects/new/', ProjectCreateView.as_view(), name='create_project'),
    # Task URLs
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/new/', TaskCreateView.as_view(), name='create_task'),
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='edit_task'),
]

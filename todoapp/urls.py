from django.urls import path
from . import views

app_name = 'todoapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('add-task/', views.add_task, name='add_task'),
    path('search-task/', views.search_task, name='search_task'),
    path('delete-task/<int:task_id>', views.delete_task, name='delete_task'),
    path('edit-task/<int:task_id>', views.edit_task, name='edit_task'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
]

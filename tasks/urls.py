from django.urls import path
from .views import NewTask, AllTasks, NewProject

app_name = 'tasks'

urlpatterns = [
    path('new/<str:jwt_token>', NewTask.as_view(), name='new_task'),
    path('all/<str:jwt_token>', AllTasks.as_view(), name='all_tasks'),
    path('new_project/<str:jwt_token>', NewProject.as_view(), name='new_project'),
]

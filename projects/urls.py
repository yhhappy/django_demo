from django.urls import path
from projects import views


urlpatterns = [
    # <int:pk>  :后面不能有空格
    path('get/', views.get_projects),
    path('post/', views.create_project),
    path('put/', views.put_project),
    path('delete/', views.delete_project),
]
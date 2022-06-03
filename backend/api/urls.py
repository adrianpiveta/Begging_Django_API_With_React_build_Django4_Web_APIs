from django.urls import path
from . import views

urlpatterns=[
    path('todos/', views.TodoList.as_view()),
    path('todos/<int:pk>', views.TodoRetrieveUpdateDestroy.as_view()),
    path('todos/<int:pk>/complete', views.TodoToggleCompleteSerializer.as_view())
]
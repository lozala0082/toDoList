from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('assignment/<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment-detail'),
    path('assignment/new/', views.AssignmentCreateView.as_view(), name='assignment-create'),
    path('assignment/<int:pk>/update/', views.AssignmentUpdateView.as_view(), name='assignment-update'),
    path('assignment/<int:pk>/delete/', views.AssignmentDeleteView.as_view(), name='assignment-delete'),
    path('assignment/<int:pk>/status/', views.update_status, name='update-status'),
    path('register/', views.register_view, name='register'),

    # API endpoints
    path('api/subtask/<int:pk>/update/', views.update_subtask, name='update-subtask'),
]
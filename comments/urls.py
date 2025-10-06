from django.urls import path
from .views import CommentListCreateView, CommentDetailView

urlpatterns = [
    path("tasks/<int:task_id>/comments/", CommentListCreateView.as_view(), name="comment-list-create"),
    path("tasks/<int:task_id>/comments/<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),
]
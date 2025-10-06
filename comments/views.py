from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Comment
from .serializers import CommentSerializer
from tasks.models import Task

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # при генерації схеми drf-yasg може викликати цей метод без kwargs
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()

        task_id = self.kwargs.get("task_id") or self.kwargs.get("task_pk")
        if not task_id:
            return Comment.objects.none()
        return Comment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        task_id = self.kwargs.get("task_id") or self.kwargs.get("task_pk")
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise ValidationError({"task": "Задача не знайдена"})
        serializer.save(user=self.request.user, task=task)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # guard для swagger/schema-gen
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()

        task_id = self.kwargs.get("task_id") or self.kwargs.get("task_pk")
        if not task_id:
            return Comment.objects.none()
        return Comment.objects.filter(task_id=task_id)
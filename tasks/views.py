from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsCreatorOrAdmin
from django.utils import timezone
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TaskFilter

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def perform_create(self, serializer):
        deadline = serializer.validated_data.get("deadline")

        if deadline and deadline <= timezone.now():
            raise serializers.ValidationError("Крайній термін має бути пізніше поточного часу.")

        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.status = Task.Status.COMPLETED
        task.save()
        return Response({"status": "Задача завершена"})


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrAdmin]
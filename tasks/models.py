from django.db import models

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Task(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "В процесі"
        COMPLETED = "completed", "Завершена"

    title = models.CharField(max_length=255, verbose_name="Назва задачі")
    description = models.TextField(blank=True, verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS,
        verbose_name="Статус"
    )

    created_by = models.ForeignKey(
        User,
        related_name="tasks_created",
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )

    assigned_to = models.ForeignKey(
        User,
        related_name="tasks_assigned",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Відповідальний"
    )

    deadline = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Крайній термін"
    )

    def __str__(self):
        return self.title

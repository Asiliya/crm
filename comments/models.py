from django.db import models
from django.conf import settings
from tasks.models import Task

User = settings.AUTH_USER_MODEL

class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name="Задача"
    )
    user = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name="Автор коментаря"
    )
    text = models.TextField(verbose_name="Текст коментаря")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")

    def __str__(self):
        return f"Коментар від {self.user} до {self.task}"

from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=Task._meta.get_field("assigned_to").remote_field.model.objects.all())

    class Meta:
        model = Task
        fields = [
            "id", "title", "description", "created_at", "updated_at",
            "deadline", "status", "created_by", "assigned_to"
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["created_by"] = request.user
        return super().create(validated_data)
import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    deadline_before = django_filters.DateTimeFilter(field_name='deadline', lookup_expr='lte')
    deadline_after = django_filters.DateTimeFilter(field_name='deadline', lookup_expr='gte')

    class Meta:
        model = Task
        fields = {
            'created_by': ['exact'],
            'assigned_to': ['exact'],
            'status': ['exact'],
        }
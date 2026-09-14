from rest_framework import serializers

from .models import Todo, TodoCategory


class TodoCategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, allow_blank=True)

    class Meta:
        model = TodoCategory
        fields = [
            'id',
            'tenant',
            'name',
            'slug',
            'description',
            'created_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'tenant', 'created_by', 'created_at', 'updated_at']


class TodoSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=TodoCategory.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Todo
        fields = [
            'id',
            'tenant',
            'department',
            'assigned_to',
            'created_by',
            'title',
            'description',
            'todo_type',
            'category',
            'priority',
            'due_date',
            'status',
            'review_comment',
            'satisfaction',
            'is_completed',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'tenant', 'created_by', 'created_at', 'updated_at', 'is_completed']

from rest_framework import serializers

from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    tenant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'tenant', 'name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'tenant', 'created_at', 'updated_at']

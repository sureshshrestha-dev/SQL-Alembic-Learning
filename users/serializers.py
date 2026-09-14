from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    tenant = serializers.PrimaryKeyRelatedField(read_only=True)
    department = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "tenant", "department", "role"]
        read_only_fields = ["id", "tenant", "department"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    tenant = serializers.PrimaryKeyRelatedField(read_only=True)
    department = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "tenant", "department", "role"]
        read_only_fields = ["tenant", "department"]

    def validate(self, attrs):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            attrs["tenant"] = request.user.tenant

            department_id = self.initial_data.get("department")
            if department_id is not None:
                department = request.user.tenant.departments.filter(id=department_id).first()
                if department is None:
                    raise serializers.ValidationError({"department": "Department must belong to your tenant."})
                attrs["department"] = department

            if request.user.role != "admin":
                raise serializers.ValidationError({"detail": "Only tenant admins can create users."})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
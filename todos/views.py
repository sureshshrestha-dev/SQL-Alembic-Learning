from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from departments.models import Department
from users.models import User

from .models import Todo, TodoCategory
from .serializers import TodoCategorySerializer, TodoSerializer


def get_todo_queryset(request):
    """Return only tasks the current user is allowed to access."""
    qs = Todo.objects.filter(tenant=request.user.tenant)

    if request.user.role == "agent":
        qs = qs.filter(Q(assigned_to=request.user) | Q(todo_type="shared"))
    elif request.user.role == "supervisor":
        qs = qs.filter(
            Q(todo_type="shared", department=request.user.department)
            | Q(todo_type="personal", assigned_to=request.user)
        )
    elif request.user.role == "admin":
        qs = qs.filter(Q(todo_type="shared") | Q(todo_type="personal", assigned_to=request.user))

    return qs


def validate_todo_payload(request, data, existing_todo=None):
    errors = {}
    tenant = request.user.tenant
    role = request.user.role

    todo_type = data.get("todo_type", getattr(existing_todo, "todo_type", "shared"))
    category_value = data.get("category", getattr(existing_todo, "category_id", None))
    department_id = data.get("department")
    assigned_to_id = data.get("assigned_to")

    if category_value not in (None, ""):
        try:
            category_id = int(category_value)
        except (TypeError, ValueError):
            errors["category"] = "Category must be a valid category ID."
        else:
            if not TodoCategory.objects.filter(id=category_id, tenant=tenant).exists():
                errors["category"] = "Category does not belong to your tenant."

    if department_id is None and existing_todo is not None:
        department_id = existing_todo.department_id

    if assigned_to_id is None and existing_todo is not None:
        assigned_to_id = existing_todo.assigned_to_id

    if department_id is not None:
        try:
            department = Department.objects.get(id=department_id, tenant=tenant)
        except Department.DoesNotExist:
            errors["department"] = "Department does not belong to your tenant."
        else:
            if role == "agent" and department != request.user.department:
                errors["department"] = "Agents can only use their own department."
            if role == "supervisor" and department != request.user.department:
                errors["department"] = "Supervisors can only manage their own department."

    if assigned_to_id is not None:
        try:
            assignee = User.objects.get(id=assigned_to_id, tenant=tenant)
        except User.DoesNotExist:
            errors["assigned_to"] = "Assigned user does not belong to your tenant."
        else:
            if role == "agent" and assignee != request.user:
                errors["assigned_to"] = "Agents can only assign tasks to themselves."
            if role == "supervisor" and assignee.department_id != request.user.department_id:
                errors["assigned_to"] = "Supervisors can only assign within their own department."

    if todo_type == "personal":
        if not assigned_to_id:
            errors["assigned_to"] = "Personal tasks must be assigned to a user."
        elif role == "agent" and int(assigned_to_id) != request.user.id:
            errors["assigned_to"] = "Agents can only create personal tasks for themselves."

    return errors


@extend_schema(
    request=TodoCategorySerializer,
    responses={
        200: TodoCategorySerializer(many=True),
        201: TodoCategorySerializer,
        400: None,
    },
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def todo_categories(request):
    if request.method == "GET":
        queryset = TodoCategory.objects.filter(tenant=request.user.tenant).order_by("name")
        serializer = TodoCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    serializer = TodoCategorySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save(tenant=request.user.tenant, created_by=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    request=TodoCategorySerializer,
    responses={
        200: TodoCategorySerializer,
        204: None,
        400: None,
        404: None,
    },
)
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def todo_category_detail(request, id):
    try:
        category = TodoCategory.objects.get(id=id, tenant=request.user.tenant)
    except TodoCategory.DoesNotExist:
        return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(TodoCategorySerializer(category).data)

    if request.method == "PUT":
        serializer = TodoCategorySerializer(category, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    if request.method == "DELETE":
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    request=TodoSerializer,
    responses={
        200: TodoSerializer(many=True),
        201: TodoSerializer,
        400: None,
    },
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def todos(request):
    if request.method == "GET":
        queryset = get_todo_queryset(request)
        serializer = TodoSerializer(queryset, many=True)
        return Response(serializer.data)

    serializer = TodoSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    validation_errors = validate_todo_payload(request, request.data)
    if validation_errors:
        return Response(validation_errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save(
        tenant=request.user.tenant,
        created_by=request.user,
    )
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    request=TodoSerializer,
    responses={
        200: TodoSerializer,
        204: None,
        400: None,
        404: None,
    },
)
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def todo_detail(request, id):
    try:
        todo = get_todo_queryset(request).get(id=id)
    except Todo.DoesNotExist:
        return Response({"detail": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(TodoSerializer(todo).data)

    if request.method == "PUT":
        serializer = TodoSerializer(todo, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validation_errors = validate_todo_payload(request, request.data, existing_todo=todo)
        if validation_errors:
            return Response(validation_errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    if request.method == "DELETE":
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

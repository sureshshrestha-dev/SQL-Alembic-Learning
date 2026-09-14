from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Department
from .serializers import DepartmentSerializer


@extend_schema(
    request=DepartmentSerializer,
    responses={
        200: DepartmentSerializer(many=True),
        201: DepartmentSerializer,
        400: None,
    },
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def departments(request):
    if request.method == 'GET':
        departments = Department.objects.filter(tenant=request.user.tenant)
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    if request.user.role != 'admin':
        return Response({"detail": "Only tenant admins can create departments."}, status=status.HTTP_403_FORBIDDEN)

    if 'tenant' in request.data and int(request.data.get('tenant')) != request.user.tenant.id:
        return Response({"tenant": "You can only create departments in your own tenant."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = DepartmentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    department = serializer.save(tenant=request.user.tenant)
    return Response(DepartmentSerializer(department).data, status=status.HTTP_201_CREATED)


@extend_schema(
    responses={
        200: DepartmentSerializer,
        404: None,
    },
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def department_detail(request, id):
    try:
        department = Department.objects.get(id=id, tenant=request.user.tenant)
    except Department.DoesNotExist:
        return Response({"detail": "Department not found or not in your tenant."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    if request.user.role != 'admin':
        return Response({"detail": "Only tenant admins can modify departments."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        if 'tenant' in request.data and int(request.data.get('tenant')) != request.user.tenant.id:
            return Response({"tenant": "You can only modify departments in your own tenant."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DepartmentSerializer(department, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    if request.method == 'DELETE':
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
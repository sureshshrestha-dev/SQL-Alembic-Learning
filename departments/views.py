from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
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
@permission_classes([AllowAny])
def departments(request):

    if request.method == 'GET':
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    serializer = DepartmentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@extend_schema(
    responses={
        200: DepartmentSerializer,
        404: None,
    },
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def department_detail(request, id):

    try:
        department = Department.objects.get(id=id)
    except Department.DoesNotExist:
        return Response(
            {"detail": "Department not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
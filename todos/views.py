from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Todo
from .serializers import TodoSerializer

@extend_schema(
    request=TodoSerializer,
    responses={
        200: TodoSerializer(many=True),
        201: TodoSerializer,
        400: None,
    },
)
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def todos(request):

    if request.method == 'GET':
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    serializer = TodoSerializer(data=request.data)

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
    request=TodoSerializer,
    responses={
        200: TodoSerializer,
        204: None,
        400: None,
        404: None,
    },
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def todo_detail(request, id):

    try:
        todo = Todo.objects.get(id=id)
    except Todo.DoesNotExist:
        return Response(
            {"detail": "Todo not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = TodoSerializer(
            todo,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    if request.method == 'DELETE':
        tenant.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
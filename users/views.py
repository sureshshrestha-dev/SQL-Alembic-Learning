from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer

@extend_schema(
    request=UserSerializer,
    responses={
        200: UserSerializer(many=True),
        201: UserSerializer,
        400: None,
    },
)
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def users(request):

    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    serializer = UserSerializer(data=request.data)

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
    request=UserSerializer,
    responses={
        200: UserSerializer,
        204: None,
        400: None,
        404: None,
    },
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def user_detail(request, id):

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(
            {"detail": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = UserSerializer(
            user,
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
        user.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
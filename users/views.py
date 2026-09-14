from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from departments.models import Department

from .models import User
from .serializers import RegisterSerializer, UserSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def users(request):
    if request.method == "GET":
        queryset = User.objects.filter(tenant=request.user.tenant)
        return Response(UserSerializer(queryset, many=True).data)

    if request.user.role != "admin":
        return Response({"detail": "Only tenant admins can create users."}, status=status.HTTP_403_FORBIDDEN)

    serializer = RegisterSerializer(data=request.data, context={"request": request})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()
    return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def user_detail(request, id):
    try:
        user = User.objects.get(id=id, tenant=request.user.tenant)
    except User.DoesNotExist:
        return Response({"detail": "User not found or not in your tenant."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(UserSerializer(user).data)

    if request.user.role != "admin":
        return Response({"detail": "Only tenant admins can update users."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "PUT":
        department_id = request.data.get("department")
        if department_id is not None:
            department = Department.objects.filter(id=department_id, tenant=request.user.tenant).first()
            if department is None:
                return Response({"department": "Department must belong to your tenant."}, status=status.HTTP_400_BAD_REQUEST)
            user.department = department

        if request.data.get("tenant") is not None and int(request.data.get("tenant")) != request.user.tenant.id:
            return Response({"tenant": "You can only assign users within your own tenant."}, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get("role") is not None:
            user.role = request.data.get("role")

        if request.data.get("username") is not None:
            user.username = request.data.get("username")

        if request.data.get("email") is not None:
            user.email = request.data.get("email")

        user.save()
        return Response(UserSerializer(user).data)

    if request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user).data,
                "message": "User created successfully",
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = User.objects.filter(username=username).first()
    if user is None or not user.check_password(password):
        return Response(
            {"detail": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
    except Exception:
        return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
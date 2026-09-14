from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from users.permissions import IsAdmin
from rest_framework.response import Response

from .models import Tenant
from .serializers import TenantSerializer

@extend_schema(
    request=TenantSerializer,
    responses={
        200: TenantSerializer(many=True),
        201: TenantSerializer,
        400: None,
    },
)
# @api_view(['GET', 'POST'])
# # @permission_classes([AllowAny])
# @permission_classes([IsAuthenticated, IsAdmin])
# def tenants(request):

#     if request.method == 'GET':
#         tenants = Tenant.objects.all()
#         serializer = TenantSerializer(tenants, many=True)
#         return Response(serializer.data)

#     serializer = TenantSerializer(data=request.data)

#     if serializer.is_valid():
#         serializer.save()
#         return Response(
#             serializer.data,
#             status=status.HTTP_201_CREATED
#         )

#     return Response(
#         serializer.errors,
#         status=status.HTTP_400_BAD_REQUEST
#     )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tenants(request):
    tenants = Tenant.objects.all()
    serializer = TenantSerializer(tenants, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def create_tenant(request):
    serializer = TenantSerializer(data=request.data)

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
    request=TenantSerializer,
    responses={
        200: TenantSerializer,
        204: None,
        400: None,
        404: None,
    },
)
@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([AllowAny])

@permission_classes([IsAuthenticated, IsAdmin])
def tenant_detail(request, id):

    try:
        tenant = Tenant.objects.get(id=id)
    except Tenant.DoesNotExist:
        return Response(
            {"detail": "Tenant not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = TenantSerializer(tenant)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = TenantSerializer(
            tenant,
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
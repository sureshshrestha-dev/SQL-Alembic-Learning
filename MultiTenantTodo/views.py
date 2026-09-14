# from django.http import HttpResponse
# from drf_spectacular.utils import extend_schema
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response

# from .models import TodoItem
# from .serializers import TodoItemSerializer


# def home(request):
#     return HttpResponse("MultiTenantTodo app is running.")


# @extend_schema(
#     request=TodoItemSerializer,
#     responses={
#         200: TodoItemSerializer(many=True),
#         201: TodoItemSerializer,
#         400: None,
#     },
# )
# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])
# def todo_list(request):
#     if request.method == 'GET':
#         todos = TodoItem.objects.all().order_by('-created_at')
#         serializer = TodoItemSerializer(todos, many=True)
#         return Response(serializer.data)

#     serializer = TodoItemSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)

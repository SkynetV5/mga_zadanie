from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializers, TaskHistorySerializers, RegisterSerializers
from rest_framework_simplejwt.tokens import RefreshToken
from simple_history.utils import update_change_reason
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.db.models import Q



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['id','status','assigned_user']
    search_fields = ['name', 'description']

    def perform_update(self, serializer, request, *args, **kwargs):
        user = self.request.user
        task = self.get_object()

        if task.assigned_user is None and not user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance = serializer.save()
        change_reason = self.request.data.get('change_reason', '')
        update_change_reason(instance, change_reason)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        if task.assigned_user is None and not request.user.is_staff:
            return Response({"detail": "Method \"DELETE\" not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Task.objects.all()
        else:
            return Task.objects.filter(Q(assigned_user=user) | Q(assigned_user=None))



class TaskHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.history.all()
    serializer_class = TaskHistorySerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['history_id','status','assigned_user', 'history_user']
    search_fields = ['name', 'description']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Task.history.all()
        else:
            return Task.history.filter(Q(assigned_user=user) | Q(assigned_user=None))

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializers

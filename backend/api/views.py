from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoToggleCompleteSerializer
from todo.models import Todo
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class TodoList(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)


class TodoToggleCompleteSerializer(generics.UpdateAPIView):
    serializer_class = TodoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.completed = not (serializer.instance.completed)
        serializer.save


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(
                username=data['username'],
                password=data['password'])
            user.save()

            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({'error': 'username em uso, escolha outro'}, status=400)

@csrf_exempt
def login(request):
    if request.method=='POST':
        data = JSONParser.parse(request)
        user = authenticate(
            request,
            username = data['username'],
            password = data['password'])
        if user is None:
            return JsonResponse(
                {'error':'Não foi possivel logar, usuario não localizado ou senha incorreta'},
                status=400)
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}
                                , status=201)
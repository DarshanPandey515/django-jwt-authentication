from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import EmplyoeeSerializer,UserSerializer
from .models import Employee
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics

# Create your views here.



class HomeView(APIView):


    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        employee_obj = Employee.objects.all()
        serializer = EmplyoeeSerializer(employee_obj,many=True)
        return Response({
            "status":200,
            "message":"Employees Data fetched.",
            "payload": serializer.data

        })

    def post(self,request):
        data = request.data
        serializer = EmplyoeeSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "status":200,
                "message":"Something went wrong.",
                "payload": serializer.errors

            })
        serializer.save()
        return Response({
            "status":200,
            "message":"Employees Data saved.",
            "payload": serializer.data
        })
    def put(self,request):
        employee_obj = Employee.objects.get(id=request.data['id'])
        serializer = EmplyoeeSerializer(employee_obj,data=request.data,partial=True)
        if not serializer.is_valid():
            return Response({
                "status":200,
                "message":"Something went wrong.",
                "payload": serializer.errors
            })
        serializer.save()
        return Response({
            "status":200,
            "message":"Successfully updated.",
            "payload": serializer.data
            })
    def delete(self,request):
        employee_obj = Employee.objects.get(id=request.data['id']).delete()
        return Response({
            "status":200,
            "message":"Successfully delete."
            })



class RegisterAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                'status': 403,
                'erros': serializer.errors,
                'message': "Something went wrong!"
            })
        serializer.save()
        user = User.objects.get(username = serializer.data['username'])
        refresh = RefreshToken.for_user(user)

        return Response({
            'user_id': user.pk,
            'username': user.username,
            'payload':serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })


# class Crudtask(generics.CreateAPIView,generics.ListAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmplyoeeSerializer



class Crudtask(generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmplyoeeSerializer
    lookup_field = 'id'
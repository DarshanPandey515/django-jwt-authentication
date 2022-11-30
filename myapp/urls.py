from django.urls import path
from myapp.views import *

urlpatterns = [
    path('',HomeView.as_view(),name="index"),
    path('register/', RegisterAPI.as_view()),
    path('crud/<str:id>/', Crudtask.as_view()),

]
from django.urls import path
from . import views

app_name = 'activity'

urlpatterns = [
    path('exam/', views.Exam.as_view(), name='exam'),
    path('assignment/', views.Assignment.as_view(), name='assignment'),
]


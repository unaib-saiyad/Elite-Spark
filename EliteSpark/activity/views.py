from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class Exam(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'activity/exam.html', {'navbar': 'exam'})


class Assignment(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'activity/assignment_list.html', {'navbar': 'assignment'})

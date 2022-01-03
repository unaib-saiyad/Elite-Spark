from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class Forum(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'forum/forum.html')


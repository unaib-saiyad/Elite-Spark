from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class Index(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'dashboard/dashboard.html')

    def post(self):
        return JsonResponse({
            'Status': True
        })


class ContactUs(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'dashboard/contactus.html')


class Credits(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'dashboard/credits.html')

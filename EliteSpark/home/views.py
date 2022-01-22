from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class Index(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'dashboard/dashboard.html', {'navbar': 'dashboard'})

    def post(self):
        return JsonResponse({
            'Status': True
        })


class ContactUs(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'dashboard/contactus.html', {'navbar': 'contactus'})


class Credits(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'dashboard/credits.html', {'navbar': 'credits'})

from django.urls import path
from . import views
app_name = 'home'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('contactus/', views.ContactUs.as_view(), name='contact'),
    path('credits/', views.Credits.as_view(), name='credits'),
]


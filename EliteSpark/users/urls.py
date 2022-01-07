from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from . import api

router = DefaultRouter()
router.register(r'data', api.StudentDataModelViewSet, basename='student-data')

app_name = 'user'
urlpatterns = [
    path('', views.UserAuth.as_view(), name='auth'),
    path('prn-auth/', views.PrnAuth.as_view(), name='prn-auth'),
    path('email-validation/', views.EmailValidation.as_view(), name='email-validation'),
    path('email-confirmation/<str:username>/<str:data>', views.EmailConfirmation.as_view(), name='email-confirmation'),
    path('reset-password/<str:username>/<str:data>', views.PasswordReset.as_view(), name='reset-password'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('forgot-password/', views.ForgotPassword.as_view(), name='forgot-password'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path(r'api/student/', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from . import api

router = DefaultRouter()
router.register(r'data', api.StudentDataModelViewSet, basename='student-data')
router.register(r'query', api.StudentSearchModelViewSet, basename='student-search')
router.register(r'receiver', api.FriendRequestModelViewSet, basename='friend-request')

app_name = 'user'
urlpatterns = [
    path('', views.UserAuth.as_view(), name='auth'),
    path('prn-auth/', views.PrnAuth.as_view(), name='prn-auth'),
    path('username-check/', views.UsernameCheck.as_view(), name='username-check'),
    path('email-validation/', views.EmailValidation.as_view(), name='email-validation'),
    path('email-confirmation/<str:username>/<str:data>', views.EmailConfirmation.as_view(), name='email-confirmation'),
    path('reset-password/<str:username>/<str:data>', views.PasswordReset.as_view(), name='reset-password'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('forgot-password/', views.ForgotPassword.as_view(), name='forgot-password'),
    path('profile/<str:username>', views.Profile.as_view(), name='profile'),
    path('get-friend-request/<str:receiver>', views.GetFriendRequestStatus.as_view(), name='get-request'),
    path('remove-friend/', views.RemoeveFriend.as_view(), name='remove-friend'),
    path('get-requested-data/<str:sender>', views.GetRequestedStatus.as_view(), name='get-requested-data'),
    path('friend-request/<str:receiver>', views.FriendRequests.as_view(), name='requests'),
    path('accept-reject-request/<str:sender>', views.ActionOnRequests.as_view(), name='accept-reject-request'),
    path(r'api/student/', include(router.urls)),
    path(r'api/search/', include(router.urls)),
    path(r'api/friend-request/', include(router.urls)),
]

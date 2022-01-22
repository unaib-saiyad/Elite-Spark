import base64
import datetime
import json
import os
import sqlite3
from io import BytesIO

from EliteSpark.settings import SECRET_KEY
from PIL import Image
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import StudentData, FriendRequest, Notification


def imgProcess(file, user, before_img):
    try:
        img = Image.open(file)
        image_format = ['JPEG', 'PNG', 'TIFF', 'EPS', 'RAW']
        if img.format in image_format:
            img.thumbnail((480, 480), Image.ANTIALIAS)
            thumbnailString = BytesIO()
            if file.size > 5242880:
                img.save(thumbnailString, 'JPEG', quality=50)
            else:
                img.save(thumbnailString, 'JPEG', quality=100)
            if before_img != 'avatar.png' and before_img != '':
                os.remove(before_img.path)
            newFile = InMemoryUploadedFile(thumbnailString, None, f'{user}.jpg', 'image/jpeg',
                                           thumbnailString,
                                           None)
            return newFile
        else:
            return None
    except:
        return None


class Profile(View):
    def get(self, *args, **kwargs):
        username = self.kwargs['username']
        user = User.objects.filter(username=username).first()
        return render(self.request, 'auth/profile.html', {'user_obj': user})

    def post(self, *args, **kwargs):
        profile = self.request.FILES.get('profile')
        roll_number = self.request.POST.get('roll-number', None)
        standard = self.request.POST.get('standard', '')
        tag = self.request.POST.get('tag', '')
        privacy = self.request.POST.get('privacy', '')
        user = self.request.user
        StudentData.objects.filter(student=user).update(roll_number=roll_number, standard=standard, tag=tag,
                                                        account_scope=privacy)
        messages.success(self.request, "Student data updated successfully...")
        student = StudentData.objects.filter(student=user).first()
        if profile and student:
            new_profile = imgProcess(profile, user, student.profile)
            if new_profile:
                student.profile = new_profile
                student.save()
            else:
                messages.error(self.request, "Something went wrong to upload image please try again!...")
        return redirect(f'http://127.0.0.1:8000/user/profile/{user.username}')


class PrnAuth(View):
    def checkPrn(self, prn):
        connection_database = sqlite3.connect('data.db')
        command = "select * from Students_Data where PRN=" + prn + " ;"
        cursor = connection_database.cursor()
        cursor.execute(command)
        data = cursor.fetchone()
        return data

    def post(self, *args, **kwargs):
        prn = self.request.POST.get('prn-number')
        data = self.checkPrn(prn)
        if data is None:
            return JsonResponse({
                'Status': False,
                'Message': "Prn doesn't exists!..."
            })
        return JsonResponse({
            'Status': True,
            'Message': "Prn exist",
            "Data": data
        })


class UsernameCheck(View):
    def get(self, *args, **kwargs):
        username = self.request.GET['username']
        if username == '':
            return JsonResponse({
                'Status': False,
                'Message': 'Username should not be blank!...'
            })
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'Status': False,
                'Message': 'Username already exists!...'
            })
        return JsonResponse({
            'Status': True,
            'Message': 'Username exists...'
        })


class UserAuth(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home:index")
        return render(self.request, 'auth/register.html')

    def post(self, *args, **kwargs):
        prn = self.request.POST.get('prn-number')
        data = PrnAuth.checkPrn(self, prn)
        if data is None:
            error = {
                'heading': "PRN Doesn't exists!...",
                'message': "please check your prn and try again later, You can click the bellow button to go back on "
                           "registration page",
                'redirect': "http://127.0.0.1:8000/user/"
            }
            return render(self.request, 'error/error.html', error)
        if StudentData.objects.filter(prn=data[0]).exists():
            return render(self.request, 'auth/login.html', {'messages': [
                {'message': "PRN already registered please login...", 'color': 'danger'}
            ]})
        return render(self.request, 'auth/email-validation.html', {'prn': data[0]})


@method_decorator(csrf_exempt, name='dispatch')
class Logout(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        auth_logout(self.request)
        messages.success(self.request, 'User logout successfully...')
        return redirect('user:login')


class Login(View):
    def post(self, *args, **kwargs):
        prn = self.request.POST.get('prn-number')
        password = self.request.POST.get('password')
        data = PrnAuth.checkPrn(self, prn)
        student = StudentData.objects.filter(prn=data[0]).first()
        if not student:
            messages.error(self.request, 'Student does not exists!...')
            return redirect("user:login")
        user = student.student
        user = authenticate(username=user.username, password=password)
        if user is None:
            messages.error(self.request, 'incorrect password!...')
            return redirect("user:login")

        auth_login(self.request, user)
        messages.success(self.request, 'Login successfully...')
        return redirect("home:index")

    def get(self, *args, **kwargs):
        return render(self.request, 'auth/login.html')


class EmailValidation(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        prn = self.request.POST.get('prn-number')
        email = self.request.POST.get('email')
        password1 = self.request.POST.get('password1')
        password2 = self.request.POST.get('password2')
        if password1 != password2 or password1 == "":
            return JsonResponse({
                'Status': False,
                'Message': 'Password should be same or not empty!...'
            })
        data = PrnAuth.checkPrn(self, prn)
        if data is None:
            return JsonResponse({
                'Status': False,
                'Message': "Prn doesn't exists or something went wrong please check your prn and try again later!..."
            })
        if User.objects.filter(email=email).exists():
            student = User.objects.filter(email=email).get()
            studentData = StudentData.objects.filter(prn=prn).first()
            if studentData.student != student:
                return JsonResponse({
                    'Status': False,
                    'Message': "Please check your credentials and try again!..."
                })
            student_authentication = authenticate(username=student.username, password=password1)
            if student_authentication is None:
                return JsonResponse({
                    'Status': False,
                    'Message': "Please check your password and try again!..."
                })
            if student.is_active:
                messages.error(self.request, 'User already verified kindly login!...')
                return JsonResponse({
                    'Status': True,
                    'Redirect': 'http://127.0.0.1:8000/user/login/'
                })
        student = User.objects.create_user(username=username, email=email, password=password1, is_active=False,
                                           first_name=data[2], last_name=data[3])
        student.save()
        StudentData.objects.create(student=student, prn=data[0], full_name=data[1], mother_name=data[4])
        verification_status = send_email(student, 'email-templates/email-validation.html')
        if verification_status is False:
            User.objects.filter(username=student.username).delete()
            return JsonResponse({
                'Status': False,
                'Message': 'Something went wrong while sending the message please check your email and try again '
                           'later!... '
            })
        messages.success(self.request, 'We have sent you an email for verification kindly check your email')
        return JsonResponse({
            'Status': True,
            'Redirect': 'http://127.0.0.1:8000/'
        })

    def get(self, *args, **kwargs):
        return render(self.request, 'auth/email-validation.html')


class EmailConfirmation(View):
    def get(self, *args, **kwargs):
        username = self.kwargs['username']
        data = self.kwargs['data']
        key = key_maker(username)
        try:
            data = key.decrypt(data.encode()).decode()
            data = json.loads(data)

            valid_time = datetime.datetime.strptime(data["valid_time"], '%Y-%m-%d %H:%M:%S.%f')

            if datetime.timedelta(0) <= valid_time - datetime.datetime.today() <= datetime.timedelta(3) and \
                    username == data['username']:
                user = User.objects.filter(username=username).get()
                user.is_active = True
                user.save()
                auth_login(self.request, user)
                messages.success(self.request, 'Congrats...Your email is successfully verified')
                return redirect('home:index')

            return render(self.request, 'error/error.html', {
                'heading': "The link is expired!...",
                'message': 'The link is expired now you can verify email by making one more link just click '
                           'bellow button and go back to email verification page!...',
                'redirect': "http://127.0.0.1:8000/user/email-validation/",
            })
        except:
            return render(self.request, 'error/error.html', {
                'heading': "Something went wrong!...",
                'message': 'Currently for the some reason link is not working please try later or make new link by '
                           'pressing the bellow button',
                'redirect': "http://127.0.0.1:8000/user/email-validation/",
            })


class ForgotPassword(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'auth/forgot_pass.html')

    def post(self, *args, **kwargs):
        prn = self.request.POST.get('prn-number')
        data = PrnAuth.checkPrn(self, prn)
        student = StudentData.objects.filter(prn=data[0]).first()
        user = student.student
        verification_status = send_email(user, 'email-templates/email-confirmation.html')
        if verification_status is False:
            return render(self.request, 'error/error.html', {
                'heading': "Error while sending email!...",
                'message': 'Something is went wrong at this point while sending the mail please try again later '
                           'click bellow button to go back to login page',
                'redirect': "http://127.0.0.1:8000/user/login/",
            })
        return render(self.request, 'error/message.html', {
            'heading': "We have send you an email!...",
            'message': 'We have send you an email kindly check your email or click bellow button to go back to login '
                       'page...',
            'redirect': "http://127.0.0.1:8000/user/login/",
        })


class PasswordReset(View):
    def get(self, *args, **kwargs):
        username = self.kwargs['username']
        data = self.kwargs['data']
        key = key_maker(username)
        try:
            data = key.decrypt(data.encode()).decode()
            data = json.loads(data)

            valid_time = datetime.datetime.strptime(data["valid_time"], '%Y-%m-%d %H:%M:%S.%f')

            if datetime.timedelta(0) <= valid_time - datetime.datetime.today() <= datetime.timedelta(3) and \
                    username == data['username']:
                return render(self.request, 'auth/gen_new_password.html', {'username': username})

            return render(self.request, 'error/error.html', {
                'heading': "The link is expired!...",
                'message': 'The link is expired now you can create new by making one more link just click '
                           'bellow button and go back to forgot password page!...',
                'redirect': "http://127.0.0.1:8000/user/forgot-password/",
            })
        except:
            return render(self.request, 'error/error.html', {
                'heading': "Something went wrong!...",
                'message': 'Currently for the some reason link is not working please try later or '
                           'pressing the bellow button to go back to dashboard',
                'redirect': "http://127.0.0.1:8000/",
            })

    def post(self, *args, **kwargs):
        password1 = self.request.POST.get('password1')
        password2 = self.request.POST.get('password2')
        username = self.request.POST.get('username')
        if password1 != password2 or password1 == "" or password2 == "":
            return render(self.request, 'auth/gen_new_password.html', {'username': username})
        if User.objects.filter(username=username).exists():
            user = User.objects.filter(username=username).get()
            try:
                message = render_to_string('email-templates/password-reset-confirmation.html', {'user': user})
                send_mail(f"{user.username} , reset password", "", "EliteSpark", [user.email, ],
                          fail_silently=False, html_message=message)
            except:
                render(self.request, 'error/error.html', {
                    'heading': "Something went wrong!...",
                    'message': 'Currently for the some reason we can not reset your password please try later or '
                               'pressing the bellow button to go back to dashboard',
                    'redirect': "http://127.0.0.1:8000/",
                })
            user.set_password(password1)
            user.save()
            messages.success(self.request, 'Password reset successfully')
            return redirect('user:login')

        return render(self.request, 'error/error.html', {
            'heading': "Something went wrong!...",
            'message': 'Currently for the some reason we can not reset your password please try later or '
                       'pressing the bellow button to go back to dashboard',
            'redirect': "http://127.0.0.1:8000/",
        })


@method_decorator(csrf_exempt, name='dispatch')
class FriendRequests(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        receiver_username = self.kwargs['receiver']
        receiver = User.objects.get(username=receiver_username)
        object, created = FriendRequest.objects.get_or_create(sender=user, receiver=receiver)
        notification, n_created = Notification.objects.get_or_create(notify_sender=user, notify_receiver=receiver,
                                                                     message='Friend Request')
        if created:
            return JsonResponse({
                'Status': True
            })
        else:
            notification.delete()
            object.delete()
            return JsonResponse({
                'Status': False
            })


@method_decorator(csrf_exempt, name='dispatch')
class GetFriendRequestStatus(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        receiver_username = self.kwargs['receiver']
        receiver = User.objects.get(username=receiver_username)
        querySet = FriendRequest.objects.filter(receiver=receiver).filter(sender=user).first()
        if querySet:
            if querySet.status:
                return JsonResponse({
                    'Status': True
                })
        return JsonResponse({
            'Status': False
        })


@method_decorator(csrf_exempt, name='dispatch')
class GetRequestedStatus(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        sender_username = self.kwargs['sender']
        sender = User.objects.get(username=sender_username)
        querySet = FriendRequest.objects.filter(sender=sender).filter(receiver=user).first()
        try:
            notification = Notification.objects.filter(notify_sender=sender).filter(notify_receiver=user) \
                .filter(message='Friend Request').get()
            notification.is_seen = True
            notification.save()
        except:
            pass
        if querySet:
            if querySet.status:
                return JsonResponse({
                    'Status': True
                })
        return JsonResponse({
            'Status': False
        })


@method_decorator(csrf_exempt, name='dispatch')
class ActionOnRequests(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        sender_username = self.kwargs['sender']
        sender = User.objects.get(username=sender_username)
        action = self.request.GET['action']
        sender_data = StudentData.objects.get(student=sender)
        receiver_data = StudentData.objects.get(student=user)
        friend_request = FriendRequest.objects.filter(sender=sender).filter(receiver=user).first()
        notification = Notification.objects.filter(notify_sender=sender).filter(notify_receiver=user) \
            .filter(message='Friend Request')
        if friend_request:
            if friend_request.status:
                friend_request.delete()
                notification.delete()
                if action == 'accept':
                    sender_data.friends.add(user)
                    receiver_data.friends.add(sender)
                return JsonResponse({
                    'Status': True
                })
        messages.info(self.request, 'User has canceled the request!...')
        return JsonResponse({
            'Status': False
        })


@method_decorator(csrf_exempt, name='dispatch')
class RemoeveFriend(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        removee_username = self.request.GET['removee']
        removee = User.objects.get(username=removee_username)
        user_data = StudentData.objects.get(student=user)
        removee_data = StudentData.objects.get(student=removee)
        user_data.friends.remove(removee)
        user_data.save()
        removee_data.friends.remove(user)
        removee_data.save()
        return JsonResponse({
            'Status': True
        })


def key_maker(username):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'\xcfz\xfc\xdcF\xc1d\xc1\xb4\xfa5%\xe7\xa5\x14\x16',
        iterations=100000,
        backend=default_backend()
    )
    return Fernet(base64.urlsafe_b64encode(kdf.derive(str(SECRET_KEY + username[::-1]).encode())))


def send_email(user, template):
    # Key Making
    key = key_maker(user.username)

    data = {
        "username": user.username,
        "valid_time": str(datetime.datetime.today() + datetime.timedelta(days=3))
    }
    data = key.encrypt(json.dumps(data).encode()).decode()
    message = render_to_string(template, {'user': user, 'data': data})
    try:
        send_mail(f"{user.username} , email verification", "", "EliteSpark", [user.email, ], fail_silently=False,
                  html_message=message)
        return True
    except:
        return False

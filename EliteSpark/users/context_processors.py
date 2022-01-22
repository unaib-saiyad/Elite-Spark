from .models import StudentData, FriendRequest


def auth_student(request):
    try:
        login_student = StudentData.objects.filter(student=request.user).first()
        return {'auth_student': login_student}
    except:
        return {'auth_student': None}



from rest_framework.authentication import SessionAuthentication
from rest_framework.viewsets import ModelViewSet

from .models import StudentData, User, FriendRequest
from .serializers import StudentDataSerilizer, FriendRequestSerilizer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class StudentDataModelViewSet(ModelViewSet):
    queryset = StudentData.objects.all()
    serializer_class = StudentDataSerilizer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)

    # pagination_class = MessagePagination
    def list(self, request, *args, **kwargs):
        username = self.request.GET['username']
        try:
            user = User.objects.filter(username=username).get()
            self.queryset = StudentData.objects.filter(student=user)
        except:
            self.queryset = StudentData.objects.filter(student=self.request.user)
        return super(StudentDataModelViewSet, self).list(request, *args, **kwargs)


class StudentSearchModelViewSet(ModelViewSet):
    queryset = StudentData.objects.all()
    serializer_class = StudentDataSerilizer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)

    # pagination_class = MessagePagination
    def list(self, request, *args, **kwargs):
        query = request.GET['query']
        if len(query) > 78:
            self.queryset = {}
        else:
            username_search_user = User.objects.filter(username__icontains=query).first()
            username_search_student = StudentData.objects.filter(student=username_search_user)
            prn_search_students = StudentData.objects.filter(prn__icontains=query)
            full_name_search_students = StudentData.objects.filter(full_name__icontains=query)
            tag_search_students = StudentData.objects.filter(tag__icontains=query)
            self.queryset = prn_search_students.union(full_name_search_students, tag_search_students,
                                                      username_search_student)
        return super(StudentSearchModelViewSet, self).list(request, *args, **kwargs)


class FriendRequestModelViewSet(ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerilizer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)

    # pagination_class = MessagePagination
    def list(self, request, *args, **kwargs):
        receiver = request.GET['receiver']
        if receiver:
            user = User.objects.get(username=receiver)
            self.queryset = FriendRequest.objects.filter(receiver=user)
        else:
            self.queryset = {}
        return super(FriendRequestModelViewSet, self).list(request, *args, **kwargs)

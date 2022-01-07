from rest_framework.authentication import SessionAuthentication
from rest_framework.viewsets import ModelViewSet

from .models import StudentData
from .serializers import StudentDataSerilizer


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
        user = self.request.user
        if user.is_authenticated:
            self.queryset = StudentData.objects.filter(student=user)
        else:
            self.queryset = {}
        return super(StudentDataModelViewSet, self).list(request, *args, **kwargs)


from rest_framework import viewsets, permissions, authentication
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import ToDo
from .serializers import ToDoSerializer

class ToDoViewSet(viewsets.ModelViewSet):
    serializer_class = ToDoSerializer
    queryset = ToDo.objects.all()

    #permessi
    permission_classes = (permissions.IsAuthenticated,)
    #autenticazione
    authentication_classes = (authentication.SessionAuthentication, authentication.TokenAuthentication)

    #@method_decorator(login_required) 
    def create(self, request):
        print(self.permission_classes)
        print(self.authentication_classes)
        return super().create(request)

    #@method_decorator(login_required) 
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

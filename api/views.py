import rest_framework.permissions
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializer import RegisterSerializer
from .renderers import UserJSONRenderer


# Create your views here.
class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    # custom render class UserJSONRender
    # renderer_classes = [UserJSONRenderer]
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

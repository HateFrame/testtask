from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_filters import rest_framework as filters

from authentication.models import User

from .serializer import RegisterSerializer, MatchSerializer, UserSerializer
from .utils import send_liked_mail


# Create your views here.
class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    ''' custom render class UserJSONRender '''
    # renderer_classes = [UserJSONRenderer]

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MatchView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MatchSerializer

    def post(self, request, id):
        user = request.user
        serializer = self.serializer_class(
            data={
                'user': user.pk,
                'partner': id
            }
        )

        if serializer.is_valid(raise_exception=True):
            partner = serializer.validated_data.get('partner')
            serializer.save(user=user, partner=partner)
            if partner.likes.filter(pk=user.pk).exists():
                # pass
                send_liked_mail(user, partner)
                send_liked_mail(partner, user)

            return Response(status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender']


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = UserFilter


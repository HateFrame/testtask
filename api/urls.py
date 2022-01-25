from django.urls import path, include
from .views import RegisterView, MatchView, UserListView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('clients/create/', RegisterView.as_view(), name='register'),
    path('clients/<int:id>/match', MatchView.as_view(), name='match'),
    path('list/', UserListView.as_view(), name='list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

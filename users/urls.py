from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentListAPIView, PaymentCreateAPIView

app_name = UsersConfig.name
router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payments'),
    path('token/', TokenObtainPairView.as_view(permission_classes=[AllowAny]), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=[AllowAny]), name='token_refresh'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
] + router.urls

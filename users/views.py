from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class UserViewSet(ModelViewSet):
    """
    ViewSet for users
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class PaymentListAPIView(ListAPIView):
    """
    ViewSet for payments
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course_paid', 'lesson_paid', 'payment_method',)
    ordering_fields = ('payment_date',)


class PaymentCreateAPIView(CreateAPIView):
    """
    Payment creates endpoint
    """
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.user = self.request.user

        course_id = self.request.data.get('course_paid')
        lesson_id = self.request.data.get('lesson_paid')
        if course_id:
            course_product = create_stripe_product(Course.objects.get(pk=course_id).title)
            course_price = create_stripe_price(instance.course_paid.amount, course_product)
            session_id, payment_link = create_stripe_session(course_price)
        else:
            lesson_product = create_stripe_product(Lesson.objects.get(pk=lesson_id).title)
            lesson_price = create_stripe_price(instance.lesson_paid.amount, lesson_product)
            session_id, payment_link = create_stripe_session(lesson_price)

        instance.session_id = session_id
        instance.payment_link = payment_link
        instance.save()

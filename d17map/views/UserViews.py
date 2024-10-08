from rest_framework import generics, status
from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.authtoken.models import Token

from d17map.models import Reservation
from d17map.serializers import ReservationSerializer, UserRegistrationSerializer


User = get_user_model()


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserReservations(generics.GenericAPIView):
    serializer_class = ReservationSerializer

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        if not user_id:
            return Response(
                {"detail": "Missing or malformed user ID"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.user.pk != int(user_id):
            return Response(
                {"detail": "You do not have permission to view these reservations."},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        reservations = Reservation.objects.filter(user=user)
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserFutureReservations(generics.GenericAPIView):
    serializer_class = ReservationSerializer

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        if not user_id:
            return Response(
                {"detail": "Missing or malformed user ID"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        today = timezone.now().date()
        reservations = Reservation.objects.filter(user=user, date__gte=today)
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            print(user, "logged")
            return Response(
                {
                    "token": token.key,
                    "userId": user.pk,
                    "userType": user.type,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

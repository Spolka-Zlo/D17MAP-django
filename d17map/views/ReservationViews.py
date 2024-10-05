from django.http import JsonResponse
from django.utils.dateparse import parse_date
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from d17map.models import Reservation, ReservationType, UserType
from d17map.serializers import (
    DayReservationSerializer,
    ReservationSerializer,
)
from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
)


class ReservationListCreate(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DayReservationList(generics.ListAPIView):
    serializer_class = DayReservationSerializer

    def get_queryset(self):
        day = self.request.query_params.get("day")
        if day:
            try:
                date = parse_date(day)
                return Reservation.objects.filter(date=date)
            except ValueError:
                return Reservation.objects.none()
        return Reservation.objects.all()


class ReservationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


permissions = {
    UserType.ADMIN.name: [
        ReservationType.CLASS,
        ReservationType.EXAM,
        ReservationType.TEST,
        ReservationType.LECTURE,
        ReservationType.CONSULTATIONS,
        ReservationType.CONFERENCE,
        ReservationType.STUDENTS_CLUB_MEETING,
        ReservationType.EVENT,
    ],
    UserType.STUDENT.name: [],
    UserType.TEACHER.name: [
        ReservationType.CLASS,
        ReservationType.EXAM,
        ReservationType.TEST,
        ReservationType.LECTURE,
        ReservationType.CONSULTATIONS,
        ReservationType.CONFERENCE,
        ReservationType.STUDENTS_CLUB_MEETING,
        ReservationType.EVENT,
    ],
    UserType.STUDENT_COUNCIL_PRESIDENT.name: [
        ReservationType.CLASS,
        ReservationType.EXAM,
        ReservationType.TEST,
        ReservationType.LECTURE,
        ReservationType.CONSULTATIONS,
        ReservationType.CONFERENCE,
        ReservationType.STUDENTS_CLUB_MEETING,
        ReservationType.EVENT,
    ],
    UserType.STUDENTS_CLUB_MEMBER.name: [
        ReservationType.CONFERENCE,
        ReservationType.STUDENTS_CLUB_MEETING,
        ReservationType.EVENT,
    ],
}


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def reservation_types_view(request):
    token = request.headers.get("Authorization")
    if not token:
        return JsonResponse({"error": "Missing token"}, status=400)
    token = token.split(" ")[1]
    user_type = Token.objects.get(key=token).user.type
    types = [tag.value for tag in permissions[user_type]]
    print(f"user_type: {user_type}")
    print(f"types: {types}")
    return JsonResponse({"types": types})

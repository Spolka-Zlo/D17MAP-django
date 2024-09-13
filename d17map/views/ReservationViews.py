from django.utils.dateparse import parse_date
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from d17map.models import Reservation
from d17map.serializers import DayReservationSerializer, ReservationSerializer


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

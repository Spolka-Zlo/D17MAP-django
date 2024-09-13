from rest_framework import generics, status
from rest_framework.response import Response

from d17map.models import Equipment
from d17map.serializers import EquipmentSerializer


class EquipmentListCreate(generics.ListCreateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EquipmentBatchCreate(generics.GenericAPIView):
    serializer_class = EquipmentSerializer

    def post(self, request, *args, **kwargs):
        names = request.data
        if not isinstance(names, list) or not all(
            isinstance(name, str) for name in names
        ):
            return Response(
                {"detail": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not names:
            return Response(
                {"detail": "Empty equipment list"}, status=status.HTTP_400_BAD_REQUEST
            )

        created_equipment_ids = []
        for name in names:
            if name.strip():
                if Equipment.objects.filter(name=name).exists():
                    continue
                equipment = Equipment.objects.create(name=name)
                created_equipment_ids.append(equipment.id)

        return Response(created_equipment_ids, status=status.HTTP_201_CREATED)

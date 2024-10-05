from rest_framework import serializers
from .models import ClassRoom, CustomUser, Equipment, Reservation
from django.contrib.auth import get_user_model


class ClassRoomSerializer(serializers.ModelSerializer):
    equipment = serializers.StringRelatedField(many=True)

    class Meta:
        model = ClassRoom
        fields = ["id", "name", "description", "capacity", "equipment"]


class SimpleClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ["id", "name"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "classroom",
            "title",
            "date",
            "startTime",
            "endTime",
            "type",
        ]


class DayReservationSerializer(serializers.ModelSerializer):
    classroom = SimpleClassRoomSerializer()

    class Meta:
        model = Reservation
        fields = ["id", "type", "startTime", "endTime", "classroom"]


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ["id", "name"]


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = CustomUser
        fields = ["username", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

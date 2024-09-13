from rest_framework import serializers
from .models import ClassRoom, CustomUser, Equipment, Reservation
from django.contrib.auth import get_user_model


class ClassRoomSerializer(serializers.ModelSerializer):
    equipments = serializers.StringRelatedField(many=True)

    class Meta:
        model = ClassRoom
        fields = ["id", "name", "description", "capacity", "equipments"]


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
        fields = ["username", "password", "email", "first_name", "last_name"]

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

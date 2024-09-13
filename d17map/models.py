from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum


class UserType(Enum):
    ADMIN = 1
    STUDENT = 2
    TEACHER = 3
    STUDENT_COUNCIL_PRESIDENT = 4
    STUDENTS_CLUB_MEMBER = 5


class CustomUser(AbstractUser):
    type = models.IntegerField(
        choices=[(tag, tag.value) for tag in UserType], default=UserType.STUDENT.value
    )


class ReservationType(Enum):
    CLASS = "class"
    EXAM = "exam"
    TEST = "test"
    LECTURE = "lecture"
    CONSULTATIONS = "consultations"
    CONFERENCE = "conference"
    STUDENTS_CLUB_MEETING = "students_club_meeting"
    EVENT = "event"


class Equipment(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    capacity = models.IntegerField()
    equipments = models.ManyToManyField(Equipment)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    date = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    type = models.CharField(
        choices=[(tag.value, tag.value) for tag in ReservationType],
        default=ReservationType.CLASS.value,
        max_length=50,
    )

from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum


class UserType(Enum):
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    STUDENT_COUNCIL_PRESIDENT = "STUDENT_COUNCIL_PRESIDENT"
    STUDENTS_CLUB_MEMBER = "STUDENTS_CLUB_MEMBER"


class CustomUser(AbstractUser):
    type = models.IntegerField(
        choices=[(tag, tag.value) for tag in UserType], default=UserType.STUDENT.value
    )


class ReservationType(Enum):
    CLASS = "Ćwiczenia"
    EXAM = "Egzamin"
    TEST = "Kolokwium"
    LECTURE = "Wykład"
    CONSULTATIONS = "Konsultacje"
    CONFERENCE = "Konferencja"
    STUDENTS_CLUB_MEETING = "Spotkanie koła naukowego"
    EVENT = "Wydarzenie"


class Equipment(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    capacity = models.IntegerField()
    equipment = models.ManyToManyField(Equipment)

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

    def __str__(self):
        return self.title

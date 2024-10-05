from django.urls import path

from d17map.views.ClassRoomViews import ClassRoomDetail, ClassRoomListCreate
from d17map.views.EquipmentViews import EquipmentBatchCreate, EquipmentListCreate
from d17map.views.ReservationViews import (
    DayReservationList,
    ReservationDetail,
    ReservationListCreate,
    reservation_types_view,
)
from d17map.views.UserViews import (
    LoginView,
    UserFutureReservations,
    UserRegistrationView,
    UserReservations,
)


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="user-registration"),
    path("classrooms/", ClassRoomListCreate.as_view(), name="classroom-list-create"),
    path("classrooms/<int:pk>/", ClassRoomDetail.as_view(), name="classroom-detail"),
    path(
        "reservations/", ReservationListCreate.as_view(), name="reservation-list-create"
    ),
    path("reservations/day/", DayReservationList.as_view(), name="day-reservations"),
    path(
        "reservations/<int:pk>/", ReservationDetail.as_view(), name="reservation-detail"
    ),
    path("reservations-types/", reservation_types_view, name="reservation-types"),
    path("equipments/", EquipmentListCreate.as_view(), name="equipment-list-create"),
    path(
        "equipments/batch/",
        EquipmentBatchCreate.as_view(),
        name="equipment-batch-create",
    ),
    path(
        "users/<int:id>/reservations/",
        UserReservations.as_view(),
        name="user-reservations",
    ),
    path(
        "users/<int:id>/future-reservations/",
        UserFutureReservations.as_view(),
        name="user-future-reservations",
    ),
]

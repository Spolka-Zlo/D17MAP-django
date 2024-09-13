from django.contrib import admin
from .models import ClassRoom, Equipment, Reservation, CustomUser

admin.site.register(CustomUser)
admin.site.register(ClassRoom)
admin.site.register(Equipment)
admin.site.register(Reservation)

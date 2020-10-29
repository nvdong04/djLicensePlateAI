from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(parking_lot)
admin.site.register(block)
admin.site.register(parking_slot)
admin.site.register(ticket_type)
admin.site.register(ticket_vehicle_type)
admin.site.register(vehicle)
admin.site.register(ticket)



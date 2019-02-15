from django.contrib import admin
from .models import Refueling
from .models import FuelPrice

admin.site.register(Refueling)
admin.site.register(FuelPrice)

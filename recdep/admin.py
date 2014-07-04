from django.contrib import admin
from recdep.models import (AccessPoint, Device, DeviceCheckin,
                           DeviceWifiCheckin, DeviceBatteryCheckin,)

for x in [AccessPoint, Device, DeviceCheckin, DeviceWifiCheckin,
          DeviceBatteryCheckin]:
    admin.site.register(x)

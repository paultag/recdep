from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import User


class AccessPoint(models.Model):
    ssid = models.CharField(max_length=128)
    bssid = models.CharField(max_length=128, unique=True)


class Place(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    point = gis_models.PointField()
    objects = gis_models.GeoManager()


class Device(models.Model):
    owner = models.ForeignKey(User, related_name='devices')
    name = models.CharField(max_length=128, unique=True)
    token = models.CharField(max_length=128)

    @property
    def checkin(self):
        try:
            return self.checkins.latest('when')
        except DeviceCheckin.DoesNotExist:
            return None


class DeviceCheckin(models.Model):
    device = models.ForeignKey(Device, related_name='checkins')
    when = models.DateTimeField(auto_now=True)

    @property
    def access_points(self):
        try:
            return self.wifi_checkins.all()
        except DeviceWifiCheckin.DoesNotExist:
            return []

    @property
    def batteries(self):
        try:
            return self.battery_checkins.all()
        except DeviceWifiCheckin.DoesNotExist:
            return []


class DeviceWifiCheckin(models.Model):
    checkin = models.ForeignKey(DeviceCheckin, related_name='wifi_checkins')
    access_point = models.ForeignKey(AccessPoint, related_name='wifi_checkins')
    strength = models.IntegerField()
    associated = models.BooleanField(default=False)


class DeviceBatteryCheckin(models.Model):
    checkin = models.ForeignKey(DeviceCheckin, related_name='battery_checkins')
    name = models.CharField(max_length=32)
    value = models.DecimalField(decimal_places=8, max_digits=8)

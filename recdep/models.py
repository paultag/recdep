from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import User


class Place(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    point = gis_models.PointField()
    objects = gis_models.GeoManager()

    @property
    def access_points(self):
        return self.aps.all()


class AccessPoint(models.Model):
    ssid = models.CharField(max_length=128)
    bssid = models.CharField(max_length=128, unique=True)
    location = models.ForeignKey(Place, related_name='aps', null=True)


class Device(models.Model):
    owner = models.ForeignKey(User, related_name='devices')
    name = models.CharField(max_length=128, unique=True)
    token = models.CharField(max_length=128)

    @property
    def location(self):
        return self.checkin.location()

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
    def location(self):
        # Find all APs with a place, sort by strength, return
        checkins = self.wifi_checkins.filter(
            access_point__isnull=False
        ).order_by('-strength')
        if checkins.count() == 0:
            return None
        checkin = checkins[0]
        return checkin.access_point.location

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
    value = models.IntegerField()

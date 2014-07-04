import json
from twilio.rest import TwilioRestClient

from django.conf import settings
from restless.modelviews import Endpoint
from restless.auth import BasicHttpAuthMixin, login_required

from .helpers import (RecDepListEndpoint, RecDepDetailEndpoint,
                      smerge, validate_machine_update)

from .models import (Device, DeviceCheckin, DeviceBatteryCheckin,
                     DeviceWifiCheckin, AccessPoint, Place)


LOCATION_SERIALIZE = {
    "include": [
        ("point", lambda x: x.point.coords),
    ],
    "exclude": [
        "id"
    ]
}


ACCESS_POINT_SERIALIZE = {
    "exclude": ["id"],
    "include": [
        ("location", LOCATION_SERIALIZE),
    ]
}


WIFI_SERIALIZE = {
    "include": [
        ("access_point", ACCESS_POINT_SERIALIZE),
    ],
}


BATTERY_SERIALIZE = {
    "include": [],
}


DEVICE_SERIALIZE = {
    "include": [
        ("owner", {"fields": ["id", "username"]}),
        ("checkin", {
            "include": [
                ("location", LOCATION_SERIALIZE),
                ("wifi_checkins", {
                    "include": [
                        ("access_point", {
                            "fields": [
                                "bssid",
                                "ssid",
                            ]
                        }),
                    ],
                    "exclude": ["id", "checkin"],
                }),
                ("batteries", smerge(BATTERY_SERIALIZE, {
                    "exclude": ["id", "checkin"]
                })),
            ],
            "exclude": [
                "device", "id", "checkin"
            ]
        }),
    ],
    "exclude": ["token"]
}


class DeviceList(RecDepListEndpoint):
    model = Device
    serialize_config = DEVICE_SERIALIZE


class DeviceDetail(RecDepDetailEndpoint):
    model = Device
    query_key = "name"
    serialize_config = DEVICE_SERIALIZE

    def load_report(self, device, report):
        when = report.pop('time')
        data = report.pop('data')
        batteries = data.pop('battery')
        access_points = data.pop('wifi')
        dc = DeviceCheckin(when=when, device=device)
        dc.save()

        for battery in batteries:
            batt = DeviceBatteryCheckin(checkin=dc, **battery)
            batt.save()

        for ap in access_points:
            try:
                dap = AccessPoint.objects.get(bssid=ap['bssid'])
            except AccessPoint.DoesNotExist:
                dap = AccessPoint(bssid=ap['bssid'], ssid=ap['ssid'])
                dap.save()

            dwc = DeviceWifiCheckin(
                checkin=dc,
                strength=ap['strength'],
                associated=ap['associated'],
                access_point=dap,
            )
            dwc.save()

    @validate_machine_update
    def post(self, request, key, **kwargs):
        data = json.loads(request.data['upload'])
        device = Device.objects.get(name=key)
        for report in data:
            self.load_report(device, report)


class PlaceList(RecDepListEndpoint):
    model = Place
    serialize_config = smerge(
        LOCATION_SERIALIZE,
        {"include": [
            ("access_points", {
                "exclude": ["id", "location"],
            }),
        ]})


class PlaceDetail(RecDepDetailEndpoint):
    model = Place
    query_key = "name"
    serialize_config = LOCATION_SERIALIZE

    @validate_machine_update
    def post(self, request, key, **kwargs):
        raise NotImplementedError("Foo")



class TextEndpoint(Endpoint, BasicHttpAuthMixin):
    methods = ["POST"]

    @login_required
    def post(self, request, *args, **kwargs):
        body = request.POST['message']

        client = TwilioRestClient(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
        )
        client.messages.create(
            to=settings.TWILIO_TO_NUMBER,
            from_=settings.TWILIO_FROM_NUMBER,
            body="""From: {user.username}

{body}""".format(user=request.user, body=body)
        )

        return {"sent": True}

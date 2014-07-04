from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.gis.geos import fromstr

from ...models import Place, AccessPoint
import yaml


class Command(BaseCommand):
    help = 'load in division-boundary mappings'

    def handle(self, *args, **options):
        for fp in args:
            with open(fp, 'r') as fd:
                datastore = yaml.load(fd)

            for data in datastore.get('places', []):
                name = data['name']
                try:
                    place = Place.objects.get(name=name)
                    print("Update place: {}".format(name))
                except Place.DoesNotExist:
                    print("New place: {}".format(name))
                    place = Place(name=name)

                lat, lon = data['location']
                point = fromstr("POINT({lon} {lat})".format(lon=lon, lat=lat))
                place.point = point
                place.description = data['description']
                place.save()

            for data in datastore.get('known_aps', []):
                place = Place.objects.get(name=data['location'])
                ssid = data['ssid']
                bssid = data['bssid']

                try:
                    ap = AccessPoint.objects.get(bssid=bssid)
                    print("Update bssid: {}".format(bssid))
                except AccessPoint.DoesNotExist:
                    print("New bssid: {}".format(bssid))
                    ap = AccessPoint(bssid=bssid)

                ap.ssid = ssid
                ap.location = place
                ap.save()

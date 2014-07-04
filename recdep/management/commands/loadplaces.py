from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.gis.geos import fromstr

from ...models import Place
import yaml


class Command(BaseCommand):
    help = 'load in division-boundary mappings'

    def handle(self, *args, **options):
        for fp in args:
            with open(fp, 'r') as fd:
                places = yaml.load(fd).get('places', [])

            for data in places:
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

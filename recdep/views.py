from restless.modelviews import ListEndpoint, DetailEndpoint
from restless.models import serialize
from restless.http import HttpError


class DeviceList(ListEndpoint):
    model = None

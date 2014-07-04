from django.core.paginator import Paginator, EmptyPage

from restless.modelviews import ListEndpoint, DetailEndpoint
from restless.models import serialize
from restless.http import HttpError
from restless.auth import BasicHttpAuthMixin, login_required

from .models import Device

import json


def smerge(dict1, dict2):
    ret = dict(dict1)
    for k, v in dict2.items():
        if k not in ret:
            ret[k] = []
        ret[k] += v
    return ret


def validate_machine_update(fn):
    def _(self, request, *args, **kwargs):
        machine = kwargs.get('key', None)
        if machine is None:
            raise HttpError(401, "No device given")

        try:
            m = Device.objects.get(name=machine)
        except Device.DoesNotExist:
            raise HttpError(401, "Bad device given")

        token = json.loads(request.data['config']).get('token', None)
        if token != m.token:
            raise HttpError(401, "Bad device given")

        return fn(self, request, *args, **kwargs)
    return _


class RecDepListEndpoint(ListEndpoint, BasicHttpAuthMixin):
    methods = ['GET']
    per_page = 100
    serialize_config = {}

    def filter(self, data, **kwargs):
        return data.filter(**kwargs)

    def sort(self, data, sort_by):
        return data.order_by(*sort_by)

    def paginate(self, data, page):
        paginator = Paginator(data, per_page=self.per_page)
        return paginator.page(page)

    @login_required
    def get(self, request, *args, **kwargs):
        params = request.params
        page = 1
        if 'page' in params:
            page = int(params.pop('page'))

        sort_by = []
        if 'sort_by' in params:
            sort_by = params.pop('sort_by').split(",")

        data = self.get_query_set(request, *args, **kwargs)
        data = self.filter(data, **params)
        data = self.sort(data, sort_by)
        try:
            data_page = self.paginate(data, page)
        except EmptyPage:
            raise HttpError(
                404,
                'No such page (heh, literally - its out of bounds)'
            )

        return {
            "meta": {
                "count": len(data_page.object_list),
                "page": page,
                "per_page": self.per_page,
                "max_page": data_page.end_index(),
                "total_count": data.count(),
                "user": {
                    "username": request.user.username,
                    "id": request.user.id
                }
            },
            "results": [
                serialize(x, **self.serialize_config)
                for x in data_page.object_list
            ]
        }


class RecDepDetailEndpoint(DetailEndpoint, BasicHttpAuthMixin):
    methods = ['GET', 'POST']
    serialize_config = {}
    query_key = None

    def post(self, request, *args, **kwargs):
        raise NotImplementedError("Not implemented")

    def get_object(self, request, key, *args, **kwargs):
        if self.query_key is None:
            raise NotImplementedError("Missing query_key")

        return self.model.objects.get(**{self.query_key: key})

    @login_required
    def get(self, request, *args, **kwargs):
        data = self.get_object(request, *args, **kwargs)
        return serialize(data, **self.serialize_config)

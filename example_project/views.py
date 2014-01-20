# -*- coding: utf-8 -*-
from django.views.generic import View
from soul.decorators import render_to
from soul.exceptions import NotFound, NotModified, Forbidden, Redirect
from test import models


class Json(View):

    @render_to('json')
    def get(self, request):
        return {"key": "value"}


class Statuses(View):

    @render_to('json')
    def get(self, request, data):
        if 'status' in data:
            if data['status'] == "301":
                raise Redirect(data['redirect'])
            elif data['status'] == "304":
                raise NotModified
            elif data['status'] == "403":
                raise Forbidden
            elif data['status'] == "404":
                raise NotFound('404.html')

        return {"info": "Send GET or application/json 'status'",
                "statuses": {
                    "301": "Redirect",
                    "304": "NotModified",
                    "403": "Forbidden",
                    "404": "NotFound"
                }}


class Models(View):

    @render_to('json')
    def get(self, request, data):
        return {
            "models": models.Test.objects.all(),
            "test": {
                "asd": models.Test.objects.all()
            }
        }


class ModelsFull(View):

    @render_to('json')
    def get(self, request, data):

        for i in range(10):
            models.Test(test_field="asd").save()

        return {"status": "saved"}

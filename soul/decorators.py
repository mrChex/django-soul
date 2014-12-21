# -*- coding: utf-8 -*-
import json
import inspect
import datetime
import decimal
from django.http import HttpResponse,\
    HttpResponseRedirect,\
    HttpResponseForbidden, \
    HttpResponseNotFound, \
    HttpResponseNotModified, \
    HttpResponseBadRequest
from django.db.models.query import QuerySet
from django.db.models.fields.files import FieldFile
from django.template import RequestContext, loader
import exceptions


def render_to(template_path, ajax_allowed=True, request_to_output=True):
    def renderer(function):
        def wrapper(self, request, *args, **kwargs):
            if "data" in inspect.getargspec(function).args:
                if request.META['CONTENT_TYPE'].startswith('application/json'):
                    request_data = json.loads(request.body)
                elif request.META['CONTENT_TYPE'].startswith('application/x-www-form-urlencoded') or request.META['CONTENT_TYPE'].startswith('text/plain'):
                    if request.method == "GET":
                        request_data = request.GET
                    elif request.method == "POST":
                        request_data = request.POST
                    else:
                        raise ValueError("Request method: %s not allowed for CONTENT_TYPE: %s" % (
                            request.method,
                            request.META['CONTENT_TYPE']))
                else:
                    raise ValueError("Unknown content type: '%s'" % request.META['CONTENT_TYPE'])
                kwargs['data'] = request_data

            try:
                out = function(self, request, *args, **kwargs)
            except exceptions.NotFound as notfound:
                return HttpResponseNotFound(loader.get_template(notfound.template).render(RequestContext(request)))
            except exceptions.Forbidden as forbidden:
                return HttpResponseForbidden(loader.get_template(forbidden.template).render(RequestContext(request)))
            except exceptions.NotModified:
                return HttpResponseNotModified()
            except exceptions.Redirect as redirect:
                return HttpResponseRedirect(redirect.path)
            except exceptions.BadRequest:
                return HttpResponseBadRequest()

            if template_path == "json" or ajax_allowed and request.is_ajax():
                def serialize_object(_obj):
                    if type(_obj) == QuerySet:
                        ignore_fields = _obj.ignore_fields if hasattr(_obj, 'ignore_fields') else False
                        return map(lambda model: model.to_dict(ignore_fields), _obj)
                    elif isinstance(_obj, decimal.Decimal):
                        return float(_obj)
                    elif isinstance(_obj, datetime.datetime):
                        return _obj.strftime('%d %m %Y %H:%M:%S')
                    elif hasattr(_obj, '__module__') and str(_obj.__module__).split('.')[1] == 'models':
                        return _obj.to_json()
                    elif isinstance(_obj, FieldFile):
                        return _obj.url if _obj else None
                    elif hasattr(_obj, 'to_dict'):
                        return _obj.to_dict()
                    else:
                        raise ValueError("Unknown response type %s" % type(_obj))

                return HttpResponse(json.dumps(out, default=serialize_object),
                                    content_type="application/json",
                                    status=200)

            else:
                if request_to_output:
                    out['request'] = request
                return HttpResponse(loader.get_template(template_path).render(RequestContext(request, out)))

        return wrapper

    return renderer
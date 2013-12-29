# -*- coding: utf-8 -*-
import json
import inspect
from django.http import HttpResponse,\
    HttpResponseRedirect,\
    HttpResponseForbidden, \
    HttpResponseNotFound, \
    HttpResponseNotModified
from django.db.models.query import QuerySet
from django.template import RequestContext, loader
import exceptions


def render_to(template_path, ajax_allowed=True, request_to_output=True):
    def renderer(function):
        def wrapper(self, request, *args, **kwargs):

            if "data" in inspect.getargspec(function).args:
                if request.META['CONTENT_TYPE'].startswith('application/json'):
                    request_data = json.loads(request.body)
                elif request.META['CONTENT_TYPE'].startswith('application/x-www-form-urlencoded'):
                    if request.method == "GET":
                        request_data = request.GET
                    elif request.method == "POST":
                        request_data = request.POST
                    else:
                        raise ValueError("Request method: %s not allowed for CONTENT_TYPE: %s" % (request.method, request.META['CONTENT_TYPE']))
                else:
                    raise ValueError("Unknown content type: '%s'" % request.META['CONTENT_TYPE'])
                kwargs['data'] = request_data

            try:
                out = function(self, request, *args, **kwargs)
            except exceptions.NotFound:
                return HttpResponseNotFound()
            except exceptions.Forbidden:
                return HttpResponseForbidden()
            except exceptions.NotModified:
                return HttpResponseNotModified()
            except exceptions.Redirect as redirect:
                return HttpResponseRedirect(redirect.path)

            if template_path == "json" or ajax_allowed and request.is_ajax():
                if type(out) in [dict, list]:
                    out_dict = json.dumps(out)
                elif type(out) == QuerySet:
                    out_dict = map(lambda model: model.to_dict(), out)
                elif hasattr(out, 'to_dict'):
                    out_dict = out.to_dict()
                else:
                    raise ValueError("Unknown response type %s" % type(out))

                return HttpResponse(json.dumps(out_dict),
                                    mimetype="application/json",
                                    status=200)

            else:
                if request_to_output:
                    out['request'] = request
                return HttpResponse(loader.get_template(template_path).render(RequestContext(request, out)))

        return wrapper

    return renderer
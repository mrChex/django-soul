from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import views

urlpatterns = patterns('',
    url(r'^json/$', views.Json.as_view()),
    url(r'^statuses/', views.Statuses.as_view()),

    url(r'^models', views.Models.as_view()),
    url(r'^models/full', views.ModelsFull.as_view())
)

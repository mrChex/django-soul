# -*- coding: utf-8 -*-
from django.db import models
from soul.models import SerializeModel


class Test(models.Model, SerializeModel):
    to_dict_fields = ['test_field']

    test_field = models.CharField(max_length=150)


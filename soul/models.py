from datetime import datetime, date
from time import mktime
from types import FunctionType
from django.db.models.query import QuerySet
from decimal import Decimal


class SerializeModel():
    to_dict_fields = []

    def to_dict(self, ignore_fields=False):
        to_return = {}
        for field_name in self.to_dict_fields:
            if ignore_fields and field_name in ignore_fields:
                continue
            field = getattr(self, field_name)

            if str(type(field)) == "<class 'django.db.models.fields.related.ManyRelatedManager'>":
                value = field.all()
            elif type(field) in (tuple, list, dict, unicode, str, int, long, type(None), bool):
                value = field
            elif type(field) == datetime or type(field) == date:
                value = mktime(field.timetuple())
            elif type(field) == Decimal:
                value = float(field)
            elif type(field) == FunctionType:
                value = field()
            elif type(field) == QuerySet:
                value = map(lambda model: model.to_dict(), field)
            else:
                if hasattr(field, "to_dict"):
                    value = field.to_dict()
                else:
                    raise Exception("Type %s not supported for serialization!" % type(field))

            to_return[field_name] = value

        return to_return
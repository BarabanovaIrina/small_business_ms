from typing import Callable

from django.db.models import Manager

from .managers import SafeGetManager


def only_objects_decorator(func: Callable):
    def only_objects_wrapper(objects, only=(), *args, **kwargs):
        return func(objects, *args, **kwargs).only(*only)

    return only_objects_wrapper


@only_objects_decorator
def all_objects(objects: Manager, only=()):
    return objects.all()


def get_object_by_id(objects: Manager, object_id):
    return objects.get(pk=object_id)


def get_object_by_id_safe(objects: SafeGetManager, object_id, model):
    return objects.safe_get(pk=object_id, model=model)


@only_objects_decorator
def filter_objects(objects: Manager, *args, **kwargs):
    return objects.filter(*args, **kwargs)

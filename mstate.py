#!/usr/bin/env python3

from functools import wraps


def decorate(target):
    target_type = type(target)

    _logs = []

    def logs_add_entry():
        entry = f"target: {repr(target)}"
        _logs.append(entry)

    def rebind(attribute):
        method = getattr(target_type, attribute)

        # not a method
        if not callable(method):
            return method

        @wraps(method)
        def new_method(*args, **kwargs):
            result = method(*args, **kwargs)
            logs_add_entry()
            return result

        # in case of static or class methods
        is_bound = getattr(method, "__get__", None) is None
        if is_bound:
            return new_method
        else:
            return new_method.__get__(target, target_type)

    class Rebinder(target_type):
        def __init__(self):
            pass

        def logs(self):
            for log in _logs:
                yield log

    for attribute in dir(target_type):
        # __getattribute__ is screwing up with subclass method access
        # needs a custom implementation
        if attribute not in ("__class__", "__init__", "__getattribute__"):
            setattr(Rebinder, attribute, rebind(attribute))

    return Rebinder()

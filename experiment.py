#!/usr/bin/env python3

from functools import wraps


def decorate(target):
    target_type = type(target)

    logs = []

    def logs_add_entry():
        entry = f"target: {repr(target)}"
        logs.append(entry)

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

    for attribute in dir(target_type):
        if attribute not in ("__class__", "__init__"):
            setattr(Rebinder, attribute, rebind(attribute))

    return Rebinder()


elements = [5]
nelements = decorate(elements)
nelements.append(10)
nelements.append(20)
nelements.append(666)

print(f"len: {len(nelements)}")
print(f"copy: {nelements}")
print(f"original: {elements}")
print("repr copy: ", repr(nelements))
print("repr original: ", repr(elements))

print("Iteration check...")
for i in nelements:
    print(f"i: {i}")

print("is instance of the same type?", isinstance(nelements, type(elements)))

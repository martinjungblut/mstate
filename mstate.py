import inspect
from functools import wraps


def watch(target, *, logs=None):
    target_type = type(target)

    if logs is None:
        logs = []

    def logs_add_entry(*, name):
        filename, linenumber = None, None

        for frame in inspect.stack():
            code_context = frame[4]
            if code_context and f".{name}" in code_context[0]:
                filename = frame[1]
                linenumber = frame[2]
                break

        entry = {
            "name": name,
            "value_after": repr(target),
            "filename": filename,
            "linenumber": linenumber,
        }

        logs.append(entry)

    def rebind(attribute):
        method = getattr(target_type, attribute)

        # not a method, just a regular attribute
        if not callable(method):
            return method

        @wraps(method)
        def new_method_unbound(*args, **kwargs):
            result = method(*args, **kwargs)
            logs_add_entry(name=method.__name__)
            return result

        @wraps(method)
        def new_method_bound(_, *args, **kwargs):
            result = method(*args, **kwargs)
            logs_add_entry(name=method.__name__)
            return result

        # in case of static or class methods
        is_bound = getattr(method, "__self__", None) is not None
        if is_bound:
            return new_method_bound
        else:
            return new_method_unbound.__get__(target, target_type)

    class Watcher(target_type):
        def __init__(self):
            pass

        def __getattr__(self, name):
            return target.__getattribute__(name)

        def ilogs(self):
            for log in logs:
                yield log

    for attribute in dir(target_type):
        # __getattribute__ impacts subclass method access
        if attribute not in ("__class__", "__init__", "__new__", "__getattribute__"):
            try:
                setattr(Watcher, attribute, rebind(attribute))
            except AttributeError as e:
                print(e)

    return Watcher()

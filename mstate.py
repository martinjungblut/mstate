from functools import wraps


def watch(target):
    target_type = type(target)

    _logs = []

    def logs_add_entry():
        entry = f"new state: {repr(target)}"
        _logs.append(entry)

    def rebind(attribute):
        method = getattr(target_type, attribute)

        # not a method, just a regular attribute
        if not callable(method):
            return method

        @wraps(method)
        def new_method_unbound(*args, **kwargs):
            result = method(*args, **kwargs)
            logs_add_entry()
            return result

        @wraps(method)
        def new_method_bound(_, *args, **kwargs):
            result = method(*args, **kwargs)
            logs_add_entry()
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

        def logs(self):
            for log in _logs:
                yield log

    for attribute in dir(target_type):
        # __getattribute__ impacts subclass method access
        if attribute not in ("__class__", "__init__", "__new__", "__getattribute__"):
            try:
                setattr(Watcher, attribute, rebind(attribute))
            except AttributeError as e:
                print(e)

    return Watcher()

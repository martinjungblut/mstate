import inspect
from functools import wraps


def watch(target_type, *, logs=None):
    if logs is None:
        logs = {}

    def logs_add_entry(*, name, target, args, kwargs):
        try:
            frameinfo = inspect.stack()[2]
        except IndexError:
            filename, linenumber = None, None
        else:
            filename = frameinfo[1]
            linenumber = frameinfo[2]

        entry = {
            "name": name,
            "value_after": repr(target),
            "args": [repr(arg) for arg in args],
            "kwargs": {key: repr(value) for key, value in kwargs.items()},
            "filename": filename,
            "linenumber": linenumber,
        }

        try:
            logs[id(target)].append(entry)
        except Exception:
            logs[id(target)] = [entry]

    def rebind(attribute):
        method = getattr(target_type, attribute)

        # not a method, just a regular attribute
        if not callable(method):
            return method

        @wraps(method)
        def new_method_bound(*args, **kwargs):
            target = args[0]
            result = method(*args, **kwargs)
            logs_add_entry(
                name=method.__name__, target=target, args=args[1:], kwargs=kwargs
            )
            return result

        @wraps(method)
        def new_method_unbound(cls, *args, **kwargs):
            target = cls
            result = method(*args, **kwargs)
            logs_add_entry(
                name=method.__name__, target=target, args=args, kwargs=kwargs
            )
            return result

        # in case of static or class methods
        is_unbound = getattr(method, "__self__", None) is not None
        if is_unbound:
            return new_method_unbound
        else:
            return new_method_bound

    class Watcher(target_type):
        def ilogs(self):
            for log in logs[id(self)]:
                yield log

    # __class__ must be a class, not a rebound method
    # __dict__ isn't writable for 'type' objects
    # __new__ is responsible for creating the new Watcher object
    # __getattribute__ impacts subclass method access
    # __repr__ is the magic method implemented to expose state transitions
    for attribute in dir(target_type):
        if attribute not in (
            "__class__",
            "__dict__",
            "__new__",
            "__getattribute__",
            "__repr__",
        ):
            try:
                setattr(Watcher, attribute, rebind(attribute))
            except Exception as exc:
                print(f"Error when setting attribute '{attribute}': {type(exc)} {exc}")

    return Watcher

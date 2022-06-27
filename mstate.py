import inspect
from functools import wraps


def watch(target, *, logs=None):
    target_type = type(target)

    if logs is None:
        logs = []

    def logs_add_entry(*, name):
        context_contains_reference = lambda *, context: f".{name}" in context[0]
        frames_with_matching_contexts = filter(
            lambda frameinfo: context_contains_reference(context=frameinfo[4]),
            inspect.stack(),
        )

        try:
            frame = next(frames_with_matching_contexts)
            filename = frame[1]
            linenumber = frame[2]
        except StopIteration:
            filename, linenumber = None, None

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
        def new_method_bound(_, *args, **kwargs):
            result = method(*args, **kwargs)
            logs_add_entry(name=method.__name__)
            return result

        @wraps(method)
        def new_method_unbound(*args, **kwargs):
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

    # __class__ must be a class, not a rebound method
    # __dict__ isn't writable for 'type' objects
    # __init__ is already being implemented on Watcher
    # __new__ is responsible for creating the new Watcher object
    # __getattribute__ impacts subclass method access
    for attribute in dir(target_type):
        if attribute not in (
            "__class__",
            "__dict__",
            "__init__",
            "__new__",
            "__getattribute__",
        ):
            setattr(Watcher, attribute, rebind(attribute))

    return Watcher()

import inspect
from functools import wraps


def watch(target_type):
    logs = {}

    def logs_add_entry(*, name, state, target, args, kwargs):
        try:
            frameinfo = inspect.stack()[2]
        except IndexError:
            filename, call_at, context_at = None, None, None
        else:
            filename = frameinfo.frame.f_code.co_filename
            call_at = frameinfo.frame.f_lineno
            context_at = frameinfo.frame.f_code.co_firstlineno

        if name == "__setattr__":
            name = "{}=".format(args[0])
            args = [args[1]]

        entry = {
            "name": name,
            "state": state,
            "args": [repr(arg) for arg in args],
            "kwargs": {repr(key): repr(value) for key, value in kwargs.items()},
            "filename": filename,
            "call_at": call_at,
            "context_at": context_at,
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
                name=method.__name__,
                state=target.instance_watch(),
                target=target,
                args=args[1:],
                kwargs=kwargs,
            )
            return result

        @wraps(method)
        def new_method_unbound(cls, *args, **kwargs):
            target = cls
            result = method(*args, **kwargs)
            logs_add_entry(
                name=method.__name__,
                state=target.class_watch(),
                target=target,
                args=args,
                kwargs=kwargs,
            )
            return result

        # in case of class methods
        is_unbound = getattr(method, "__self__", None) is not None
        if is_unbound:
            return new_method_unbound
        else:
            return new_method_bound

    class WatcherProtocol:
        def instance_watch(self):
            raise NotImplementedError

        @classmethod
        def class_watch(cls):
            raise NotImplementedError

    class Watcher(target_type, WatcherProtocol):
        def ilogs(self):
            try:
                for log in logs[id(self)]:
                    yield log
            except KeyError:
                pass

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
            "instance_watch",
            "class_watch",
        ):
            setattr(Watcher, attribute, rebind(attribute))

    return Watcher

import inspect
from functools import wraps


def _method_is(type_a, method, type_b):
    try:
        reference = type_a.__dict__[method.__name__]
    except KeyError:
        return False
    else:
        return isinstance(reference, type_b)


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
            "context_at": context_at,
            "state": state,
            "type": target_type,
            "name": name,
            "args": [repr(arg) for arg in args],
            "kwargs": {repr(key): repr(value) for key, value in kwargs.items()},
            "filename": filename,
            "call_at": call_at,
        }

        target_id = id(target)
        try:
            logs[target_id].append(entry)
        except Exception:
            logs[target_id] = [entry]

    def rebind(attribute_name):
        attribute = getattr(target_type, attribute_name)

        @wraps(attribute)
        def new_method(*args, **kwargs):
            target = args[0]
            result = attribute(*args, **kwargs)
            logs_add_entry(
                name=attribute.__name__,
                state=target.instance_watch(),
                target=target,
                args=args[1:],
                kwargs=kwargs,
            )
            return result

        @wraps(attribute)
        def new_classmethod(cls, *args, **kwargs):
            result = attribute(*args, **kwargs)
            logs_add_entry(
                name=attribute.__name__,
                state=cls.class_watch(),
                target=cls,
                args=args,
                kwargs=kwargs,
            )
            return result

        if not callable(attribute):
            return attribute
        elif _method_is(target_type, attribute, staticmethod):
            return
        elif _method_is(target_type, attribute, classmethod):
            return new_classmethod
        else:
            return new_method

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

        def shared_logs(self):
            for key, value in logs.items():
                yield key, value

    # __class__ must be a class, not a rebound method
    # __dict__ isn't writable for 'type' objects
    # __new__ is responsible for creating the new Watcher object
    # __getattribute__ causes a RecursionError if rebound
    # __repr__ causes a RecursionError if rebound
    # instance_watch and class_watch are part of the protocol
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
            new_attribute = rebind(attribute)
            if new_attribute is not None:
                setattr(Watcher, attribute, new_attribute)

    return Watcher

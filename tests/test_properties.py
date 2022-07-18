from mstate import watch


@watch
class Counter:
    def __init__(self):
        self._value = 0

    @property
    def increment(self):
        self._value = self._value + 1
        return self._value

    def instance_watch(self):
        return repr({"value": self._value})


def test():
    counter = Counter()
    assert counter.increment == 1
    assert counter.increment == 2
    assert counter.increment == 3

    # __init__ adds an extra read, so the length is 5
    assert len([*counter.ilogs()]) == 5

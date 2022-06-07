#!/usr/bin/env python3

import inspect
from dataclasses import dataclass
from functools import wraps


@dataclass
class LogEntry:
    value_repr: str
    location: str

    def __eq__(self, other):
        return self.value_repr == other


def MState(*, logs=True):
    _bindings, _logs = {}, {}

    def _refresh_logs(name):
        if not logs:
            return

        location = f"{name} {name}"
        for frame in inspect.stack():
            if f".{name}" in frame[4][0]:
                location = "{}:{}".format(frame[1], frame[2])
                break

        value_repr = repr(_bindings[name])
        log_entry = LogEntry(value_repr=value_repr, location=location)

        try:
            if _logs[name][-1] != value_repr:
                _logs[name].append(log_entry)
        except KeyError:
            _logs[name] = [log_entry]

    class State:
        def __setattr__(self, name, value):
            _bindings[name] = value
            _refresh_logs(name)

        def __getattr__(self, name):
            value = _bindings[name]

            class StateWrapper:
                def __getattr__(self, iname):
                    iattr = getattr(value, iname)
                    if not callable(iattr):
                        return iattr

                    @wraps(iattr)
                    def new_callable(*args, **kwargs):
                        result = iattr(*args, **kwargs)
                        _refresh_logs(name)
                        return result

                    return new_callable

                def __getitem__(self, *args, **kwargs):
                    return value.__getitem__(*args, **kwargs)

            try:
                return StateWrapper()
            except KeyError as e:
                raise AttributeError(e)

        def print_logs(self):
            for name, entries in _logs.items():
                for entry in entries:
                    print(name, entry.value_repr, entry.location)

    return State


def mstate(*, logs=True):
    return MState(logs=logs)()


class Player(MState()):
    def __init__(self, name, age, race):
        self.name = name
        self.age = age
        self.race = race
        self.items = []


def chain_a(p):
    chain_b(p)


def chain_b(p):
    chain_c(p)


def chain_c(p):
    p.age = 50
    p.website = "http://debian.org"


if __name__ == "__main__":
    player = Player("Martin", 30, "Human")
    player.name = "Martin J. Schreiner"
    player.age = 31

    player.items.append("Sword")
    player.items.append("Shield")
    player.items.append("Helmet")

    chain_a(player)
    player.print_logs()

    print("------------------")

    st = mstate(logs=True)
    st.name = "Martin"
    st.age = 30
    st.age = 31
    st.name = "Martin J. Schreiner"
    st.items = []
    st.items.append(10)
    st.items.append(20)

    st.items.append(30)
    st.items.append(40)
    st.items.pop()
    st.items = st.items[::-1]
    st.print_logs()

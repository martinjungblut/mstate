#!/usr/bin/env python3


def MState(*, logs=True):
    _bindings, _logs = {}, {}

    class State:
        def __setattr__(self, name, value):
            _bindings[name] = value
            self._refresh_logs()

        def __getattr__(self, name):
            self._refresh_logs()

            try:
                return _bindings[name]
            except KeyError as e:
                raise AttributeError(e)

        def _refresh_logs(self):
            if not logs:
                return

            for name, value in _bindings.items():
                value_repr = repr(value)

                try:
                    if _logs[name][-1] != value_repr:
                        _logs[name].append(value_repr)
                except KeyError:
                    _logs[name] = [value_repr]

        def print_logs(self):
            self._refresh_logs()

            for name, values in _logs.items():
                for value in values:
                    print(name, value)

    return State


def mstate(*, logs=True):
    return MState(logs=logs)()


class Player(MState()):
    def __init__(self, name, age, race):
        self.name = name
        self.age = age
        self.race = race
        self.items = []


if __name__ == "__main__":
    player = Player("Martin", 30, "Human")
    player.name = "Martin J. Schreiner"
    player.age = 31
    player.items.append("Sword")

    breakpoint()

    # st = mstate(logs=True)
    # st.name = "Martin"
    # st.age = 30
    # st.age = 31
    # st.name = "Martin J. Schreiner"
    # st.items = []
    # st.items.append(10)
    # st.items.append(20)
    # st.items.append(30)
    # st.items.append(40)
    # st.items.pop()
    # st.items = st.items[::-1]

    # st.print_logs()

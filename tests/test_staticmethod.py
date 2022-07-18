from mstate import watch

SWITCHES = {"website": "http://www.debian.org"}


@watch
class Switch:
    @staticmethod
    def exists(name):
        return name in SWITCHES


def test():
    assert Switch.exists("website")
    assert not Switch.exists("owner")

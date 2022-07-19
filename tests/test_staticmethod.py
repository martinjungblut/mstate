from mstate import watch

SWITCHES = {"website": "http://www.debian.org"}


@watch
class Switch:
    def instance_watch(self):
        return repr(SWITCHES)

    @staticmethod
    def exists(name):
        return name in SWITCHES

    def website_exists(self):
        return self.exists("website")


class TestStaticMethod:
    def test_staticmethod(self):
        assert Switch.exists("website")
        assert not Switch.exists("owner")

    def test_staticmethod_via_instance_reference(self):
        switch = Switch()
        assert switch.website_exists()

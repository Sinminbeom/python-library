from python_library.singleton.singleton import Singleton


class SingletonTest(Singleton):
    def __init__(self):
        pass


def test_singleton():
    singleton1 = SingletonTest.instance()
    singleton2 = SingletonTest.instance()
    assert singleton1 == singleton2

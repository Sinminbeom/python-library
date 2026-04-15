from python_library.thread.thread import abThread


class ThreadTest(abThread):
    def __init__(self):
        super().__init__()
        pass

    def action(self) -> None:
        print("ThreadTest!")
        pass


class ThreadingTest(abThread):
    def __init__(self):
        super().__init__()
        pass

    def action(self) -> None:
        print("ThreadTest!")
        pass


def test_thread():
    thread_test = ThreadTest()
    thread_test.start()
    pass


def test_threading():
    threading = ThreadingTest()
    threading.start()
    pass

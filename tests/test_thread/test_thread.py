from python_library.thread.thread import abThread, abThreading


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


class RaisingThread(abThread):
    def __init__(self):
        super().__init__()
        self.caught: list[Exception] = []

    def action(self) -> None:
        raise ValueError("boom")

    def on_exception(self, e: Exception) -> None:
        self.caught.append(e)


def test_on_exception_called_on_single_shot():
    # on_exception을 오버라이드해 삼키면(다시 던지지 않으면) 예외가 잡힌다
    thread = RaisingThread()
    thread.start()
    thread.join()

    assert len(thread.caught) == 1
    assert isinstance(thread.caught[0], ValueError)
    assert not thread.is_alive()


class DefaultThread(abThread):
    def action(self) -> None:
        raise ValueError("boom")


def test_default_on_exception_reraises(monkeypatch):
    # 기본 on_exception은 예외를 다시 던진다(fail-loud) → threading.excepthook으로 전달
    import threading

    caught: list[BaseException] = []
    monkeypatch.setattr(
        threading, "excepthook", lambda args: caught.append(args.exc_value)
    )

    thread = DefaultThread()
    thread.start()
    thread.join()

    assert len(caught) == 1
    assert isinstance(caught[0], ValueError)
    assert not thread.is_alive()


class RaisingThreading(abThreading):
    def __init__(self):
        super().__init__()
        self.caught: list[Exception] = []

    def action(self) -> None:
        raise ValueError("boom")

    def on_exception(self, e: Exception) -> None:
        self.caught.append(e)
        if len(self.caught) >= 3:
            self.stop()


def test_loop_continues_when_on_exception_swallows():
    # on_exception을 오버라이드해 삼키면 루프가 멈추지 않고 계속된다 (opt-in resilient)
    thread = RaisingThreading()
    thread.start()
    thread.join()

    assert len(thread.caught) == 3
    assert not thread.is_alive()

import time

from python_library.process.process import abProcessing


class SleepingProcessing(abProcessing):
    def action(self) -> None:
        time.sleep(0.01)


def test_stop_before_start_is_preserved():
    process = SleepingProcessing()
    process.stop()
    process.start()
    process.join(timeout=5)

    assert process.exitcode == 0

import time
import os

from python_library.job.job import IJob
from python_library.process.multi_process_manager import MultiProcessManager
from python_library.process.process import abProcess


class TestJob(IJob):
    def __init__(self):
        super().__init__()

    def execute(self) -> None:
        pass


class TestProcess(abProcess):
    def __init__(self):
        super().__init__()
        pass

    def action(self) -> None:
        while True:
            time.sleep(1)

            job = self.pop_shared_queue(self.name)
            # job = self.pop_shared_job_queue()
            if job is None:
                continue

            print(f"pid : {os.getpid()}")

            job.execute()


class TestMultiProcessManager(MultiProcessManager):
    def __init__(self):
        super().__init__()
        pass

    def action(self) -> None:
        while True:
            time.sleep(1)

            job = self.pop_shared_queue(self.name)

            if job is None:
                continue

            job.execute()


def main():
    process1 = TestProcess()
    process2 = TestProcess()

    multi_process_manager = TestMultiProcessManager()
    multi_process_manager.append(process1)
    multi_process_manager.append(process2)

    # multi_process_manager.push_shared_job_queue(TestJob())
    # multi_process_manager.push_shared_job_queue(TestJob())
    # multi_process_manager.push_shared_job_queue(TestJob())

    multi_process_manager.push_shared_queue("TestProcess1", TestJob())
    multi_process_manager.push_shared_queue("TestProcess2", TestJob())
    multi_process_manager.push_shared_queue("TestMultiProcessManager1", TestJob())
    #
    # multi_process_manager.push_shared_queue("process2", TestJob())
    # multi_process_manager.push_shared_queue("process2", TestJob())
    # multi_process_manager.push_shared_queue("process2", TestJob())

    multi_process_manager.start()

    while True:
        time.sleep(2)


if __name__ == "__main__":
    main()

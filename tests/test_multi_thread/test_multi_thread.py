import time

from python_library.job.job import IJob
from python_library.thread.multi_thread_manager import MultiThreadManager
from python_library.thread.worker_thread import abWorkerThread


class TestJob(IJob):
    def __init__(self):
        super().__init__()

    def execute(self) -> None:
        print("TestJob execute!!!")
        pass


class TestWorkerThread(abWorkerThread):
    def __init__(self) -> None:
        super().__init__()

    def action(self) -> None:
        while True:
            time.sleep(1)

            # print(f"@@@@@ Thread ID: {threading.get_ident()}")
            # job = self.pop_shared_job_queue()

            print(f"{self.name} || is_running = {self.is_running()}")
            # print(f"{self.name} || is_alive = {self.is_alive()}")
            # print(f"{self.name} || is_stop = {self.is_stop()}")

            job = self.pop_shared_queue(self.name)

            if job is None:
                continue

            job.execute()
            pass


class TestMultiThreadManager(MultiThreadManager):
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
    multi_thread_manager = TestMultiThreadManager()

    thread1 = TestWorkerThread()
    thread2 = TestWorkerThread()
    thread3 = TestWorkerThread()
    thread4 = TestWorkerThread()

    multi_thread_manager.append(thread1)
    multi_thread_manager.append(thread2)
    multi_thread_manager.append(thread3)
    multi_thread_manager.append(thread4)

    # multi_thread_manager.push_shared_job_queue(TestJob())
    # multi_thread_manager.push_shared_job_queue(TestJob())
    # multi_thread_manager.push_shared_job_queue(TestJob())
    # multi_thread_manager.push_shared_job_queue(TestJob())

    multi_thread_manager.push_shared_queue("TestWorkerThread1", TestJob())
    multi_thread_manager.push_shared_queue("TestWorkerThread2", TestJob())
    multi_thread_manager.push_shared_queue("TestWorkerThread3", TestJob())
    multi_thread_manager.push_shared_queue("TestWorkerThread4", TestJob())

    multi_thread_manager.push_shared_queue("TestMultiThreadManager1", TestJob())

    multi_thread_manager.start()

    while True:
        time.sleep(5)
        print("!!!!!!!!!!!!!!!!!!!")


if __name__ == "__main__":
    main()

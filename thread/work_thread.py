import time

from job_queue.job_queue import IJobQueue
from thread.thread import abThread


class WorkThread(abThread):
    def __init__(self, job_queue: IJobQueue) -> None:
        super().__init__()
        self._job_queue: IJobQueue = job_queue

    def action(self):
        while True:
            job = self._job_queue.pop()

            if job is None:
                break

            # print(f"thread id: {threading.get_ident()}")

            job.execute()

            time.sleep(0)

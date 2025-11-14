import time


class IJob:
    def execute(self) -> None:
        pass


class Job(IJob):
    def execute(self) -> None:
        print("job!!!!!!!!!!!!!!!!!!!!")
        time.sleep(3)
        pass

from abc import abstractmethod, ABC


class IJob(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class Job(IJob):
    def execute(self) -> None:
        pass

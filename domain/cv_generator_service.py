import abc
from dataclasses import dataclass
from domain.cv import CV


@dataclass
class CVGeneratorService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate(self, cv: CV) -> str:
        raise NotImplementedError

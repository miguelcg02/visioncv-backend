import abc
from typing import List
from dataclasses import dataclass
from domain.data_formatter_service import CVDateNamePlaceField


@dataclass
class CVGeneratorService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate(
        self,
        name: str,
        phone: str,
        address: str,
        email: str,
        experience: List[CVDateNamePlaceField],
        education: List[CVDateNamePlaceField],
        skills: List[str]
    ) -> str:
        raise NotImplementedError

import abc
from dataclasses import dataclass
from typing import List
from domain.cv import DateNamePlaceField


@dataclass
class DataFormatterService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_experience_section(
            self, experience: str) -> List[DateNamePlaceField]:
        raise NotImplementedError

    @abc.abstractmethod
    def create_education_section(
            self, education: str) -> List[DateNamePlaceField]:
        raise NotImplementedError

    @abc.abstractmethod
    def create_skills_section(
            self, skills: str) -> List[str]:
        raise NotImplementedError

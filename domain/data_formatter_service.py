import abc
from dataclasses import dataclass
from typing import List


@dataclass
class CVDateNamePlaceField:
    date: str
    name: str
    place: str
    description: str


@dataclass
class DataFormatterService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_experience_section(
            self, experience: str) -> List[CVDateNamePlaceField]:
        raise NotImplementedError

    @abc.abstractmethod
    def create_education_section(
            self, education: str) -> List[CVDateNamePlaceField]:
        raise NotImplementedError

    @abc.abstractmethod
    def create_skills_section(
            self, skills: str) -> List[str]:
        raise NotImplementedError

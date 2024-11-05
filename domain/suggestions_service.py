import abc
from dataclasses import dataclass


@dataclass
class SuggestionsService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def suggest_from_experience(
            self, experience: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def suggest_from_education(
            self, education: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def suggest_from_skills(
            self, skills: str) -> str:
        raise NotImplementedError

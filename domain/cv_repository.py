import abc
from typing import List
from domain.cv import CV


class CVRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save(self, cv: CV) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, cv_id) -> CV:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self, user_id) -> List[dict[str, str]]:
        raise NotImplementedError

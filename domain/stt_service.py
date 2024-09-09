import abc
from dataclasses import dataclass


@dataclass
class STTService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def transcribe(self, audio_data: bytes) -> str:
        raise NotImplementedError

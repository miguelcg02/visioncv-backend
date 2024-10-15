from dataclasses import dataclass


@dataclass
class FormDTO:
    name: str
    phone: str
    address: str
    email: str
    experience_audio: bytes
    education_audio: bytes

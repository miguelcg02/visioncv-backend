from typing import List
from dataclasses import dataclass


@dataclass
class DateNamePlaceField:
    date: str
    name: str
    place: str
    description: str


@dataclass
class PersonalInfo():
    name: str
    phone: str
    address: str
    email: str


@dataclass
class CV():
    id: str
    user_id: str
    name: str
    personal_info: PersonalInfo
    experience: List[DateNamePlaceField]
    education: List[DateNamePlaceField]
    skills: List[str]

from dataclasses import dataclass


@dataclass
class PersonalDetails:
    name: str
    phone: str
    address: str
    email: str


@dataclass
class FormDTO:
    personal_details: PersonalDetails
    experience: str
    education: str
    skills: str

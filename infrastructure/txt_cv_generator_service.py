from typing import List
from dataclasses import dataclass
from domain.cv_generator_service import CVGeneratorService
from domain.data_formatter_service import CVDateNamePlaceField


@dataclass
class TxtCVGeneratorService(CVGeneratorService):
    def generate(
        self,
        name: str,
        phone: str,
        address: str,
        email: str,
        experience: List[CVDateNamePlaceField],
    ) -> str:
        cv = (
            f"Name: {name}\n"
            f"Phone: {phone}\n"
            f"Address: {address}\n"
            f"Email: {email}\n\n")

        for exp in experience:
            cv += (
                f"Date: {exp.date}\n"
                f"Name: {exp.name}\n"
                f"Place: {exp.place}\n"
                f"Description: {exp.description}")

        path = "/static/cv.txt"
        with open(f"./{path}", 'w', encoding="utf-8") as file:
            file.write(cv)
        return path

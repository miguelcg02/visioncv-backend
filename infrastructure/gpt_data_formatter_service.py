import json
from typing import List, Dict
from dataclasses import dataclass, field
from openai import OpenAI
from domain.cv import DateNamePlaceField
from domain.data_formatter_service import DataFormatterService


@dataclass
class GPTDataFormatterService(DataFormatterService):
    client: OpenAI
    model: str = field(default="gpt-3.5-turbo")

    def __format_data(
            self, task: str, data_format: str, data: str) -> Dict:
        prompt = (
            f"{task}:\n\n"
            "Deberás responder solo en formato JSON con los siguientes "
            "campos:\n"
            f"{data_format}\n\n"
            "Esta es la información que debes transcribir:\n\n"
            "\"\"\"\n"
            f"{data}"
            "\"\"\"\n"
        )

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt},
            ]
        )

        response = completion.choices[0].message.content

        if not response:
            return {}

        try:
            response = response.replace("```json", "").replace("```", "")
            return json.loads(response)
        except Exception as e:
            raise ValueError("Error parsing data") from e

    def create_experience_section(
            self, experience: str) -> List[DateNamePlaceField]:
        experience_array = self.__format_data(
            task=("Eres un asistente de recursos humanos y tienes que "
                  "transcribir la experiencia laboral de un candidato"),
            data_format=("campos:\nexperiencias: array de experiencias\n\n"
                         "Cada experiencia cuenta con los siguientes datos:\n"
                         "date: Fecha de inicio y fin del trabajo\n"
                         "name: Nombre de la empresa\n"
                         "place: Lugar de trabajo\n"
                         "description: Descripción del trabajo\n\n"),
            data=experience)
        return [
            DateNamePlaceField(
                date=exp["date"],
                name=exp["name"],
                place=exp["place"],
                description=exp["description"]
            )
            for exp in experience_array["experiencias"]
        ]

    def create_education_section(
            self, education: str) -> List[DateNamePlaceField]:
        education_array = self.__format_data(
            task=("Eres un asistente de recursos humanos y tienes que "
                  "transcribir la educación de un candidato"),
            data_format=("campos:\neducation: array de educación\n\n"
                         "Cada educación cuenta con los siguientes datos:\n"
                         "date: Fecha de inicio y fin del estudio\n"
                         "name: Nombre de la institución\n"
                         "place: Lugar de estudio\n"
                         "description: Descripción del estudio\n\n"),
            data=education)
        return [
            DateNamePlaceField(
                date=exp["date"],
                name=exp["name"],
                place=exp["place"],
                description=exp["description"]
            )
            for exp in education_array["education"]
        ]

    def create_skills_section(
            self, skills: str) -> List[str]:
        skills_array = self.__format_data(
            task=("Eres un asistente de recursos humanos y tienes que "
                  "transcribir las habilidades de un candidato"),
            data_format=("campos:\nskills: array de habilidades\n\n"),
            data=skills)
        return skills_array["skills"]

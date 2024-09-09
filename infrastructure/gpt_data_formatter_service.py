import json
from typing import List, Dict
from dataclasses import dataclass, field
from openai import OpenAI
from domain.data_formatter_service import (
    DataFormatterService, CVDateNamePlaceField)


@dataclass
class GPTDataFormatterService(DataFormatterService):
    client: OpenAI
    model: str = field(default="gpt-3.5-turbo")

    def __get_experience_array(self, experience: str) -> List[Dict[str, str]]:
        prompt = (
            "Eres un asistente de recursos humanos y tienes que "
            "transcribir la experiencia laboral de un candidato:\n\n"
            "Deberás responder solo en formato JSON con los siguientes "
            "campos:\nexperiencias: array de experiencias\n\n"
            "Cada experiencia cuenta con los siguientes datos:\n"
            "date: Fecha de inicio y fin del trabajo\n"
            "name: Nombre de la empresa\n"
            "place: Lugar de trabajo\n"
            "description: Descripción del trabajo\n\n"
            "A continuación la experiencia laboral del candidato:\n"
            "\"\"\"\n"
            f"{experience}"
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
            return []

        try:
            response = response.replace("```json", "").replace("```", "")
            return json.loads(response)["experiencias"]
        except Exception as e:
            raise ValueError("Error parsing experience") from e

    def create_experience_section(
            self, experience: str) -> List[CVDateNamePlaceField]:
        experience_array = self.__get_experience_array(experience)
        return [
            CVDateNamePlaceField(
                date=exp["date"],
                name=exp["name"],
                place=exp["place"],
                description=exp["description"]
            )
            for exp in experience_array
        ]

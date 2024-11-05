from dataclasses import dataclass, field
from openai import OpenAI
from domain.suggestions_service import SuggestionsService


@dataclass
class GPTSuggestionsService(SuggestionsService):
    client: OpenAI
    model: str = field(default="gpt-3.5-turbo")

    def __prompt(
            self, section: str, data: str) -> str:
        prompt = (
            f"Se te va a pasar un texto conteniendo lo que "
            f"una persona dice sobre {section}:\n\n"
            "Debes dar tips sobre que se puede mejorar en este campo,"
            " no debes dar tips sobre ortografía o gramática,"
            " solo sobre cosas que vale la pena agregar o quitar.\n\n"
            "IMPORTANTE: La sugerencia no debe ser más larga que 100 palabras."
            "\n\n"
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
            raise ValueError("Error getting response")

        try:
            return response
        except Exception as e:
            raise ValueError("Error parsing data") from e

    def suggest_from_experience(
            self, experience: str) -> str:
        experience_suggestions = self.__prompt(
            section="su experiencia laboral",
            data=experience)

        return experience_suggestions

    def suggest_from_education(
            self, education: str) -> str:
        education_suggestions = self.__prompt(
            section="su educación",
            data=education)

        return education_suggestions

    def suggest_from_skills(
            self, skills: str) -> str:
        skills_suggestions = self.__prompt(
            section="sus habilidades",
            data=skills)

        return skills_suggestions

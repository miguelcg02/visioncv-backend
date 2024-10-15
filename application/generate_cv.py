from dataclasses import dataclass
from domain.stt_service import STTService
from domain.cv_generator_service import CVGeneratorService
from domain.data_formatter_service import DataFormatterService
from .dtos.form_dto import FormDTO


@dataclass
class GenerateCV:
    form_dto: FormDTO
    stt_service: STTService
    data_formatter_service: DataFormatterService
    cv_generator_service: CVGeneratorService

    def generate(self):
        experience = self.data_formatter_service.create_experience_section(
            self.form_dto.experience)

        education = self.data_formatter_service.create_education_section(
            self.form_dto.education)

        skills = self.data_formatter_service.create_skills_section(
            self.form_dto.skills)

        cv = self.cv_generator_service.generate(
            self.form_dto.personal_details.name,
            self.form_dto.personal_details.phone,
            self.form_dto.personal_details.address,
            self.form_dto.personal_details.email,
            experience,
            education,
            skills)

        return cv

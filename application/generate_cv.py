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
        experience_str = self.stt_service.transcribe(
            self.form_dto.experience_audio)
        experience = self.data_formatter_service.create_experience_section(
            experience_str)
        education_str = self.stt_service.transcribe(
            self.form_dto.education_audio)
        education = self.data_formatter_service.create_education_section(
            education_str)

        cv = self.cv_generator_service.generate(
            self.form_dto.name,
            self.form_dto.phone,
            self.form_dto.address,
            self.form_dto.email,
            experience,
            education
        )
        return cv

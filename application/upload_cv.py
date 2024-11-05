import uuid
from dataclasses import dataclass
from domain.cv import CV, PersonalInfo
from domain.cv_repository import CVRepository
from domain.stt_service import STTService
from domain.cv_generator_service import CVGeneratorService
from domain.data_formatter_service import DataFormatterService
from .dtos.form_dto import FormDTO


@dataclass
class UploadCV:
    form_dto: FormDTO
    stt_service: STTService
    data_formatter_service: DataFormatterService
    cv_generator_service: CVGeneratorService
    cv_repository: CVRepository

    def __personal_info_mapper(self, personal_info):
        return PersonalInfo(
            name=personal_info.name,
            phone=personal_info.phone,
            address=personal_info.address,
            email=personal_info.email
        )

    def upload(self, user_id):
        experience = self.data_formatter_service.create_experience_section(
            self.form_dto.experience)

        education = self.data_formatter_service.create_education_section(
            self.form_dto.education)

        skills = self.data_formatter_service.create_skills_section(
            self.form_dto.skills)

        cv = CV(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=self.form_dto.cv_name,
            personal_info=self.__personal_info_mapper(
                self.form_dto.personal_details),
            experience=experience,
            education=education,
            skills=skills)

        return self.cv_repository.save(cv)

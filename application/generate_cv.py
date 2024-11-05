from dataclasses import dataclass
from domain.cv_repository import CVRepository
from domain.cv_generator_service import CVGeneratorService


@dataclass
class GenerateCV:
    cv_id: str
    cv_generator_service: CVGeneratorService
    cv_repository: CVRepository

    def generate(self):
        cv = self.cv_repository.get(self.cv_id)
        cv_path = self.cv_generator_service.generate(cv)
        return cv_path

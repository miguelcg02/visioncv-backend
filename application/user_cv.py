from dataclasses import dataclass
from domain.cv_repository import CVRepository


@dataclass
class UserCVs:
    user_id: str
    cv_repository: CVRepository

    def get(self):
        cvs = self.cv_repository.get_all(self.user_id)
        return cvs

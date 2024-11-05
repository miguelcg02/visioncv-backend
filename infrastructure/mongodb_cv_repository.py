from dataclasses import asdict, dataclass
from typing import List
from pymongo import MongoClient
from bson.objectid import ObjectId
from domain.cv import CV, DateNamePlaceField, PersonalInfo
from domain.cv_repository import CVRepository


@dataclass
class MongoDBCVRepository(CVRepository):
    client: MongoClient
    db_name: str = "cv"
    collection_name: str = "cv"

    # Create a new CV in the database and return its id
    def save(self, cv: CV) -> str:
        cv_dict = asdict(cv)
        cv_dict.pop("id")
        result = self.client[self.db_name][self.collection_name].insert_one(
            cv_dict)
        return str(result.inserted_id)

    def get(self, cv_id) -> CV:
        cv_dict = self.client[self.db_name][self.collection_name].find_one(
            {"_id": ObjectId(cv_id)})
        if cv_dict is None:
            cv_dict = {}
        cv_dict["id"] = str(cv_dict.pop("_id"))
        cv_dict["personal_info"] = PersonalInfo(**cv_dict.pop("personal_info"))
        cv_dict["experience"] = [DateNamePlaceField(**exp)
                                 for exp in cv_dict["experience"]]
        cv_dict["education"] = [DateNamePlaceField(**edu)
                                for edu in cv_dict["education"]]

        return CV(**cv_dict)

    def get_all(self, user_id) -> List[dict[str, str]]:
        cv_dicts = self.client[self.db_name][self.collection_name].find(
            {"user_id": user_id})
        cv_dicts = [{"cv_name": str(cv_dict.pop("name")),
                     "id": str(cv_dict.pop("_id"))}
                    for cv_dict in cv_dicts]

        return cv_dicts

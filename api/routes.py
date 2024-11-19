from decouple import os
from dotenv import load_dotenv
from fastapi import APIRouter, File, UploadFile, Response, status, Depends
from fastapi_clerk_auth import (
    ClerkConfig,
    ClerkHTTPBearer,
    HTTPAuthorizationCredentials)
from api.di import (
    get_generate_cv_use_case,
    get_user_cvs_use_case,
    whisper_stt_service,
    gpt_suggestions_service,
    get_upload_cv_use_case)
from application.dtos.form_dto import FormDTO


router = APIRouter()


load_dotenv()
jwks_url = os.getenv("JWKS_URL")
clerk_config = ClerkConfig(
    jwks_url=jwks_url if jwks_url else "",)

clerk_auth_guard = ClerkHTTPBearer(config=clerk_config)


@router.get("/cv/download/{cv_id}")
async def download_cv(
        cv_id: str,
        credentials: HTTPAuthorizationCredentials | None = Depends(
            clerk_auth_guard)
):
    try:
        if credentials is None:
            return {"success": False,
                    "error": "No se encontraron credenciales"}
        cv_path = get_generate_cv_use_case(cv_id).generate()
        return {"success": True,
                "data": {"cv_path": cv_path}}
    except Exception as e:
        print(e)
        return {"success": False,
                "error": "Ocurrió un error al descargar el CV"}


@router.get("/cv/all")
async def get_user_cvs(
        credentials: HTTPAuthorizationCredentials | None = Depends(
            clerk_auth_guard)
):
    try:
        if credentials is None:
            return {"success": False,
                    "error": "No se encontraron credenciales"}
        user_id = credentials.model_dump()["decoded"]["sub"]
        cvs = get_user_cvs_use_case(user_id).get()
        return {"success": True,
                "data": {"cvs": cvs}}
    except Exception as e:
        print(e)
        return {"success": False,
                "error": "Ocurrió un error al descargar el CV"}


@router.post("/form/upload")
async def upload_form(
        form_dto: FormDTO,
        credentials: HTTPAuthorizationCredentials | None = Depends(
            clerk_auth_guard)
):
    try:
        if credentials is None:
            return {"success": False,
                    "error": "No se encontraron credenciales"}
        cv_id = get_upload_cv_use_case(form_dto).upload(
            credentials.model_dump()["decoded"]["sub"])

        return {"success": True,
                "data": {"cv_id": cv_id}}
    except Exception as e:
        print(e)
        return {"success": False,
                "error": "Ocurrió un error al generar el CV"}


@router.post("/form/experience", status_code=status.HTTP_200_OK)
async def upload_experience(
    response: Response,
    audio: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials | None = Depends(
        clerk_auth_guard)
):
    try:
        if credentials is None:
            return {"success": False,
                    "error": "No se encontraron credenciales"}

        audio_bytes = await audio.read()
        text = whisper_stt_service.transcribe(audio_bytes)
        suggestions = gpt_suggestions_service.suggest_from_experience(text)

        return {"success": True, "data": {
            "experience": text,
            "suggestions": suggestions
        }}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(e)
        return {"success": False,
                "error": ("Ocurrió un error al transcribir el audio, "
                          "inténtalo de nuevo")}


@router.post("/form/education", status_code=status.HTTP_200_OK)
async def upload_education(
    response: Response,
    audio: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials | None = Depends(
        clerk_auth_guard)
):
    try:
        if credentials is None:
            return {"success": False,
                    "error": "No se encontraron credenciales"}

        audio_bytes = await audio.read()
        text = whisper_stt_service.transcribe(audio_bytes)
        suggestions = gpt_suggestions_service.suggest_from_education(text)

        return {"success": True, "data": {
            "education": text,
            "suggestions": suggestions
        }}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(e)
        return {"success": False,
                "error": ("Ocurrió un error al transcribir el audio, "
                          "inténtalo de nuevo")}


@router.post("/form/skills", status_code=status.HTTP_200_OK)
async def upload_skills(
    response: Response,
    audio: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials | None = Depends(
        clerk_auth_guard)
):
    try:
        if credentials is None:
            return {"success": False,
                    "error": "No se encontraron credenciales"}

        audio_bytes = await audio.read()
        text = whisper_stt_service.transcribe(audio_bytes)
        suggestions = gpt_suggestions_service.suggest_from_skills(text)

        return {"success": True, "data": {
            "skills": text,
            "suggestions": suggestions
        }}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(e)
        return {"success": False,
                "error": ("Ocurrió un error al transcribir el audio, "
                          "inténtalo de nuevo")}

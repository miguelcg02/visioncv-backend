from decouple import os
from dotenv import load_dotenv
from fastapi import APIRouter, File, UploadFile, Response, status, Depends
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer, HTTPAuthorizationCredentials
from api.di import get_generate_cv_use_case, whisper_stt_service
from application.dtos.form_dto import FormDTO


router = APIRouter()


load_dotenv()
jwks_url = os.getenv("JWKS_URL")
clerk_config = ClerkConfig(
    jwks_url=jwks_url if jwks_url else "",)

clerk_auth_guard = ClerkHTTPBearer(config=clerk_config)


@router.post("/form/upload")
async def upload_form(
        form_dto: FormDTO,
        credentials: HTTPAuthorizationCredentials | None = Depends(
            clerk_auth_guard)
):
    try:
        generate_cv_use_case = get_generate_cv_use_case(form_dto)

        # add db logic to store the form data
        print(credentials)
        return {"success": True,
                "data": {"cv_path": generate_cv_use_case.generate()}}
    except Exception:
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
        audio_bytes = await audio.read()
        text = whisper_stt_service.transcribe(audio_bytes)

        # add db logic to store the experience
        print(credentials)
        return {"success": True, "data": {"experience": text}}
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
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
        audio_bytes = await audio.read()
        text = whisper_stt_service.transcribe(audio_bytes)

        # add db logic to store the education
        print(credentials)
        return {"success": True, "data": {"education": text}}
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
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
        audio_bytes = await audio.read()
        text = whisper_stt_service.transcribe(audio_bytes)

        # add db logic to store the skills
        print(credentials)
        return {"success": True, "data": {"skills": text}}
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False,
                "error": ("Ocurrió un error al transcribir el audio, "
                          "inténtalo de nuevo")}

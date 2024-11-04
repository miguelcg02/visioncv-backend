from fastapi import APIRouter, File, UploadFile, Response, status
from api.di import get_generate_cv_use_case, whisper_stt_service
from application.dtos.form_dto import FormDTO


router = APIRouter()


@router.post("/form/upload")
async def upload_form(form_dto: FormDTO):
    try:
        generate_cv_use_case = get_generate_cv_use_case(form_dto)

        return {"success": True,
                "data": {"cv_path": generate_cv_use_case.generate()}}
    except Exception:
        return {"success": False,
                "error": "Ocurrió un error al generar el CV"}


@router.post("/form/experience", status_code=status.HTTP_200_OK)
async def upload_experience(
    response: Response,
    audio: UploadFile = File(...)
):
    try:
        audio_bytes = await audio.read()
        text = whisper_stt_service.transcribe(audio_bytes)
        return {"success": True, "data": {"experience": text}}
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False,
                "error": ("Ocurrió un error al transcribir el audio, "
                          "inténtalo de nuevo")}


@router.post("/form/education", status_code=status.HTTP_200_OK)
async def upload_education(
    response: Response,
    audio: UploadFile = File(...)
):
    try:
        audio_bytes = await audio.read()
        text = whisper_stt_service.transcribe(audio_bytes)
        return {"success": True, "data": {"education": text}}
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False,
                "error": ("Ocurrió un error al transcribir el audio, "
                          "inténtalo de nuevo")}


@router.post("/form/skills", status_code=status.HTTP_200_OK)
async def upload_skills(
    response: Response,
    audio: UploadFile = File(...)
):
    try:
        audio_bytes = await audio.read()
        text = whisper_stt_service.transcribe(audio_bytes)
        return {"success": True, "data": {"skills": text}}
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False,
                "error": ("Ocurrió un error al transcribir el audio, "
                          "inténtalo de nuevo")}

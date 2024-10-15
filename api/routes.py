import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from fastapi import APIRouter, File, UploadFile, Response, status
from application.dtos.form_dto import FormDTO
from application.generate_cv import GenerateCV
from infrastructure.whisper_stt_service import WhisperSTTService
from infrastructure.pdf_cv_generator_service import PdfCVGeneratorService
from infrastructure.gpt_data_formatter_service import GPTDataFormatterService


router = APIRouter()

load_dotenv()
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
open_ai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=azure_endpoint if azure_endpoint else ""
)
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

gpt_data_formatter_service = GPTDataFormatterService(
    open_ai_client, deployment if deployment else "gtp-4o")
whisper_stt_service = WhisperSTTService(open_ai_client)
pdf_cv_generator_service = PdfCVGeneratorService()


@router.post("/form/upload")
async def upload_form(form_dto: FormDTO):
    generate_cv_use_case = GenerateCV(
        form_dto,
        whisper_stt_service,
        gpt_data_formatter_service,
        pdf_cv_generator_service
    )

    return {"cv_path": generate_cv_use_case.generate()}


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

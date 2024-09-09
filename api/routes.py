import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from fastapi import APIRouter, File, UploadFile, Form
from application.dtos.form_dto import FormDTO
from application.generate_cv import GenerateCV
from infrastructure.whisper_stt_service import WhisperSTTService
# from infrastructure.txt_cv_generator_service import TxtCVGeneratorService
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
# txt_cv_generator_service = TxtCVGeneratorService()
pdf_cv_generator_service = PdfCVGeneratorService()


@router.post("/form/upload")
async def upload_form(
    name: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    email: str = Form(...),
    experience_audio: UploadFile = File(...)
):
    audio = await experience_audio.read()
    form_dto = FormDTO(name, phone, address, email, audio)
    generate_cv_use_case = GenerateCV(
        form_dto,
        whisper_stt_service,
        gpt_data_formatter_service,
        pdf_cv_generator_service
    )

    cv_path = generate_cv_use_case.generate()

    response = {"cv_path": cv_path}

    return response

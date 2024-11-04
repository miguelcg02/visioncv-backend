"""
File for managing the dependency injection of the application
"""
from decouple import os
from dotenv import load_dotenv
from openai import AzureOpenAI

from application.generate_cv import GenerateCV
from infrastructure.gpt_data_formatter_service import GPTDataFormatterService
from infrastructure.pdf_cv_generator_service import PdfCVGeneratorService
from infrastructure.whisper_stt_service import WhisperSTTService


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


def get_generate_cv_use_case(form_dto):
    return GenerateCV(
        form_dto,
        whisper_stt_service,
        gpt_data_formatter_service,
        pdf_cv_generator_service
    )

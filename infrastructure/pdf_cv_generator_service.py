from typing import List
from dataclasses import dataclass
import pdfkit
from domain.cv_generator_service import CVGeneratorService
from domain.data_formatter_service import CVDateNamePlaceField


@dataclass
class PdfCVGeneratorService(CVGeneratorService):
    def __generate_subsection(self, title, place, date, description):
        return f"""
            <div class="subsection">
                <h3> {title} - {place}</h3>
                <p>{date}</p>
                <p>{description}</p>
            </div>\n"""

    def generate(
        self,
        name: str,
        phone: str,
        address: str,
        email: str,
        experience: List[CVDateNamePlaceField],
    ) -> str:

        template_path = './infrastructure/templates/cv.html'
        with open(template_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        html_content = html_content.replace("{{ name }}", name)
        html_content = html_content.replace("{{ phone }}", phone)
        html_content = html_content.replace("{{ email }}", email)
        html_content = html_content.replace("{{ address }}", address)

        options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': "UTF-8",
            # Enable access to local files if using images or stylesheets
            'enable-local-file-access': None
        }

        experience_html = ""
        for exp in experience:
            experience_html += self.__generate_subsection(
                exp.name, exp.place, exp.date, exp.description)
        html_content = html_content.replace(
            "{{ experience }}", experience_html)

        path = "/static/cv.pdf"
        pdfkit.from_string(html_content, f"./{path}", options=options)
        return path

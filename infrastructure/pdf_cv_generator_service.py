from typing import List
from dataclasses import dataclass
import pdfkit
from domain.cv_generator_service import CVGeneratorService
from domain.data_formatter_service import CVDateNamePlaceField


@dataclass
class PdfCVGeneratorService(CVGeneratorService):
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

    def __generate_name_date_section(self, title, place, date, description):
        return f"""
            <div class="subsection">
                <h3> {title} - {place}</h3>
                <p>{date}</p>
                <p>{description}</p>
            </div>\n"""

    def __add_name_date_section(self, html_str, section_data, section_name):
        data_html = ""
        for datum in section_data:
            data_html += self.__generate_name_date_section(
                datum.name, datum.place, datum.date, datum.description)
        return html_str.replace(
            "{{ "+section_name+" }}", data_html)

    def generate(
        self,
        name: str,
        phone: str,
        address: str,
        email: str,
        experience: List[CVDateNamePlaceField],
        education: List[CVDateNamePlaceField],
    ) -> str:

        template_path = './infrastructure/templates/cv.html'
        with open(template_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        html_content = html_content.replace("{{ name }}", name)
        html_content = html_content.replace("{{ phone }}", phone)
        html_content = html_content.replace("{{ email }}", email)
        html_content = html_content.replace("{{ address }}", address)

        html_content = self.__add_name_date_section(
            html_content, experience, "experience")

        html_content = self.__add_name_date_section(
            html_content, education, "education")

        path = "static/cv.pdf"
        pdfkit.from_string(html_content, f"./{path}", options=self.options)
        return path

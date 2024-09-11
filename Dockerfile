FROM python:3.12.4-slim-bullseye


# Install wkhtmltopdf and other dependencies
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /back
COPY . /back

RUN pip install poetry

RUN poetry install

CMD ["poetry", "run", "python", "main.py"]

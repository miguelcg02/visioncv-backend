# Vision CV - Backend

Make sure you have the following installed:
- **[Python](https://www.python.org/downloads/)** (version 3.12 or later)
- **[Poetry](https://python-poetry.org/docs/#installation)** (the dependency management tool for Python)
- **[Wkhtmltopdf](https://wkhtmltopdf.org/downloads.html)** (the tool used to convert HTML to PDF)

## Installation

Clone the repository to your local machine:
```bash
git clone https://github.com/miguelcg02/visioncv-backend
cd visioncv-backend
```

Install the dependencies:
```bash
poetry install
```

Activate the virtual environment:
```bash
poetry shell
```

## Running the server
To run the server, execute:
```bash
poetry run python main.py
```

## How to add a new dependency
To add a new dependency, execute:
```bash
poetry add <dependency>
```

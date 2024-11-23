# CV Builder API

A FastAPI-based service that processes PDF CVs/resumes using OpenAI's GPT-3.5 Turbo model to extract and structure information.

## Features

- PDF text extraction using pdfplumber
- Structured CV analysis using OpenAI GPT-3.5 Turbo
- FastAPI-based REST API
- Real-time processing with automatic server reload

## Setup

1. Clone the repository:
```bash
git clone [your-repo-url]
cd cv-builder
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install fastapi uvicorn python-dotenv openai pdfplumber
```

4. Create a .env file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

5. Run the server:
```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`

## API Endpoints

### POST /upload-cv/
Upload a PDF CV for analysis. Returns structured information about the CV including:
- Personal Details
- Professional Summary
- Employment History
- Education
- Skills
- Projects
- Certifications
- Languages
- References

### GET /
Welcome endpoint to verify the API is running.

## Requirements
- Python 3.8+
- FastAPI
- Uvicorn
- OpenAI
- pdfplumber
- python-dotenv

## License
MIT

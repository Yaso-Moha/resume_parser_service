# Career Navigator — Resume Parser Service

This service handles resume processing for the Career Navigator system.  
It extracts text from PDF/DOCX files, identifies key information, and returns structured results to the frontend.

## Features

- Accepts PDF or DOCX resume uploads  
- Extracts text, experience, and skills  
- Generates role recommendations  
- Lightweight Flask API  
- Simple to run locally

## Requirements

Install all dependencies:

```bash
pip install -r requirements.txt

## Running the Service

Start the server with:

```bash
python3 resume_parser_service.py

The API will run at:

http://localhost:5000


## API Endpoint

### POST /upload_resume

Uploads a resume file (PDF or DOCX) and returns extracted information.

Example usage:

```bash
curl -X POST -F "file=@resume.pdf" http://localhost:5000/upload_resume

{
  "skills": [...],
  "experience": [...],
  "summary": "...",
  "recommended_roles": [...]
}

## Frontend Connection

This service is used by the main Career Navigator web application:

https://github.com/Yaso-Moha/ai-career-navigator

---

## License

MIT License

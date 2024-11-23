from fastapi import FastAPI, File, UploadFile, HTTPException
import pdfplumber
import dotenv
from openai import OpenAI
import os

app = FastAPI()

dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
async def root():
    return {"message": "Welcome to ResumeBeast!"}

def send_to_openai(cv_text: str):
    """Send CV text to OpenAI for processing"""
    print("\n[OpenAI] Sending CV text to OpenAI for processing...")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": os.getenv("SYSTEM_PROMPT")},
                {"role": "user", "content": cv_text}
            ]
        )
        print("[OpenAI] Successfully received response from OpenAI")
        return response.choices[0].message.content
    except Exception as e:
        print(f"[OpenAI] Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing with OpenAI: {str(e)}")

@app.post("/upload-cv/")
async def upload_cv(file: UploadFile = File(...)):
    print(f"\n[Upload] Received file: {file.filename}")
    
    # Check file type
    if not file.filename.endswith(".pdf"):
        print("[Upload] Error: File is not a PDF")
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        # Read the uploaded file
        print("[Upload] Reading file contents...")
        contents = await file.read()

        # Parse the PDF text using pdfplumber
        print("[Parser] Starting PDF text extraction...")
        with pdfplumber.open(file.file) as pdf:
            extracted_text = ""
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"[Parser] Processing page {page_num}/{len(pdf.pages)}")
                extracted_text += page.extract_text()

        if not extracted_text.strip():
            print("[Parser] Error: Extracted text is empty")
            raise HTTPException(status_code=400, detail="The PDF appears to be empty or not readable.")
        
        print(f"[Parser] Successfully extracted {len(extracted_text)} characters")
        
        # Send to OpenAI and get response
        openai_response = send_to_openai(extracted_text)
        print("\n[Response] OpenAI Analysis:")
        print("------------------------")
        print(openai_response)
        print("------------------------")

        return {
            "filename": file.filename,
            "text": extracted_text,
            "analysis": openai_response
        }
    except Exception as e:
        print(f"[Error] An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")

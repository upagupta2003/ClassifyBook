import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
from inference_pipeline import InferencePipeline

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Maximum file size (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes
MODEL_NAME = "microsoft/Multilingual-MiniLM-L12-H384"
MODEL_PATH = "microsoft/Multilingual-MiniLM-L12-H384"

# Initialize InferencePipeline
inference_pipeline = InferencePipeline(MODEL_NAME, MODEL_PATH)

@app.post("/upload-book/")
async def upload_book(file: UploadFile = File(...)):
    # Check if the file is a PDF
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Check file size
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size should not exceed 5MB")
    
    # Process the PDF
    try:
        pdf_reader = PyPDF2.PdfReader(file.file)
        # For simplicity, we're just reading the first page
        first_page = pdf_reader.pages[0]
        text = first_page.extract_text()
        
        # Use InferencePipeline to predict genres
        genres = inference_pipeline.run(text)
        
        return JSONResponse(content={
            "filename": file.filename,
            "genres": genres
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

# Serve static files
static_files_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "build")
app.mount("/", StaticFiles(directory=static_files_dir, html=True), name="static")

# Add a root endpoint for health checks
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
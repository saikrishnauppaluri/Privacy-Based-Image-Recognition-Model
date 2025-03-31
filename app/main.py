from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from werkzeug.utils import secure_filename  # For sanitizing filenames
import aiofiles
from app.model import process_image
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Define folder paths from .env
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./uploads/")
MASKS_FOLDER = os.getenv("MASKS_FOLDER", "./outputs/")
PREDICTOR_PATH = os.getenv("PREDICTOR_PATH")
MODEL_PATH = os.getenv("MODEL_PATH")

# Create necessary folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MASKS_FOLDER, exist_ok=True)

# Serve static files (masks and UI)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/outputs", StaticFiles(directory=MASKS_FOLDER), name="outputs")


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serve the HTML UI with clean and modern design"""
    return FileResponse("app/static/index.html")


@app.post("/detect/")
async def detect_defect(file: UploadFile = File(...)):
    """Process uploaded image and generate defect mask"""
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    # Sanitize filename
    sanitized_filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, sanitized_filename)

    # Save uploaded file asynchronously
    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            content = await file.read()
            await buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Process image and generate defect mask
    try:
        mask_path = process_image(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    if mask_path:
        mask_url = f"/outputs/{os.path.basename(mask_path)}"
        return JSONResponse(content={"mask_url": mask_url, "message": "Defect mask generated successfully!"})
    else:
        raise HTTPException(status_code=400, detail="Failed to generate mask.")
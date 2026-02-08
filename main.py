from fastapi import FastAPI, UploadFile, File
import shutil
import os
from scanner_engine import run_security_scan

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "SentinelCode AI API is online"}

@app.post("/scan")
async def scan_file(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    scan_results = run_security_scan(temp_path)
    
    if os.path.exists(temp_path):
        os.remove(temp_path)
    
    return {
        "filename": file.filename,
        "analysis": scan_results
    }
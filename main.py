import whisper
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
import uvicorn

app = FastAPI(title="Whisper Transcription API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Whisper Transcription API"}

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File phải là định dạng âm thanh")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_path = temp_file.name
        content = await file.read()
        temp_file.write(content)
    try:
        model = whisper.load_model("tiny")
        result = model.transcribe(temp_path, language="vi")
        transcript = result["text"]
        segments = [{"start": s["start"], "end": s["end"], "text": s["text"]} for s in result["segments"]]
        return JSONResponse(content={"transcript": transcript, "segments": segments})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi xử lý âm thanh: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
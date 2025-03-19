import whisper
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile

# Khởi tạo FastAPI
app = FastAPI(title="Whisper Transcription API")

# Load model Whisper (dùng model "base" để nhẹ hơn khi deploy miễn phí)
model = whisper.load_model("base")

@app.get("/")
def read_root():
    return {"message": "Welcome to Whisper Transcription API"}

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    API nhận file âm thanh và trả về transcript.
    """
    # Kiểm tra file có hợp lệ không
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File phải là định dạng âm thanh")

    # Tạo file tạm để lưu file upload
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_path = temp_file.name
        # Ghi dữ liệu từ file upload vào file tạm
        content = await file.read()
        temp_file.write(content)

    try:
        # Transcribe file âm thanh bằng Whisper
        result = model.transcribe(temp_path, language="vi")  # Ngôn ngữ tiếng Việt
        transcript = result["text"]
        
        # (Tùy chọn) Lấy thêm timestamps nếu cần
        segments = [
            {
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            }
            for segment in result["segments"]
        ]

        # Trả về kết quả
        return JSONResponse(content={
            "transcript": transcript,
            "segments": segments
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi xử lý âm thanh: {str(e)}")
    finally:
        # Xóa file tạm sau khi xử lý
        if os.path.exists(temp_path):
            os.remove(temp_path)

# Chạy server (dùng khi test local)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
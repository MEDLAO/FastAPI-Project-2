import io
import os
import qrcode
import tempfile
from fastapi import FastAPI, Query, Response, Request
from fastapi.responses import JSONResponse, StreamingResponse


app = FastAPI()


RAPIDAPI_SECRET = os.getenv("RAPIDAPI_SECRET")


@app.middleware("http")
async def enforce_rapidapi_usage(request: Request, call_next):
    rapidapi_proxy_secret = request.headers.get("X-RapidAPI-Proxy-Secret")

    if rapidapi_proxy_secret != RAPIDAPI_SECRET:
        return JSONResponse(status_code=403, content={"error": "Access restricted to RapidAPI users only."})

    return await call_next(request)


@app.get("/")
def read_root():
    welcome_message = (
        "Welcome!"
        "¡Bienvenido!"
        "欢迎!"
        "नमस्ते!"
        "مرحبًا!"
        "Olá!"
        "Здравствуйте!"
        "Bonjour!"
        "বাংলা!"
        "こんにちは!"
    )
    return {"message": welcome_message}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/generate_qr/")
def generate_qr(
    text: str = Query(..., description="Text or URL to encode in QR Code"),
    download: bool = False
):
    """Generates a QR code from the given text or URL."""
    qr = qrcode.make(text)

    if download:
        # ✅ Create a temporary file to store the QR code
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            qr.save(temp_file, format="PNG")
            temp_file_path = temp_file.name  # Get file path

        # ✅ Serve the QR code as a file download
        return FileResponse(
            path=temp_file_path,
            media_type="image/png",
            filename="qr_code.png"
        )

    # ✅ If not downloading, return the QR code as an inline image
    img_io = io.BytesIO()
    qr.save(img_io, format="PNG")
    img_io.seek(0)

    return StreamingResponse(img_io, media_type="image/png")
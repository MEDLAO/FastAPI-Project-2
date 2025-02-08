import io
import os
import qrcode
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, Response


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
    request: Request,
    text: str = Query(..., description="Text or URL to encode in QR Code")
):
    """Generates a QR code, returns the image, and provides a download link."""
    qr = qrcode.make(text)

    # Create an in-memory buffer for the QR code image
    img_io = io.BytesIO()
    qr.save(img_io, format="PNG")
    img_io.seek(0)

    # Construct the download link (same endpoint but forces file download)
    base_url = str(request.base_url).rstrip("/")
    download_url = f"{base_url}/generate_qr/?text={text}"

    # Always return the image with Content-Disposition: attachment
    response = Response(
        content=img_io.getvalue(),
        media_type="image/png",
        headers={
            "Content-Disposition": 'attachment; filename="qr_code.png"',
            "X-Download-URL": download_url,  # Custom header with the link
        }
    )

    return response

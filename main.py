import io
import os
import qrcode
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, StreamingResponse


app = FastAPI()


RAPIDAPI_SECRET = os.getenv("RAPIDAPI_SECRET")


@app.middleware("http")
async def enforce_rapidapi_usage(request: Request, call_next):
    # Bypass authentication for the /welcome endpoint
    if request.url.path == "/":
        return await call_next(request)

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
def generate_qr(text: str = Query(..., description="Text or URL to encode in QR Code")):
    """Generates a QR code and returns it as an image."""

    qr = qrcode.make(text)

    # Create an in-memory buffer for the QR code image
    img_io = io.BytesIO()
    qr.save(img_io, format="PNG")
    img_io.seek(0)

    # Return the QR code as an image
    return StreamingResponse(img_io, media_type="image/png")

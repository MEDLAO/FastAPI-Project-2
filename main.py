import io
import os
import qrcode
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
def generate_qr(text: str = Query(..., description="Text or URL to encode in QR Code"), download: bool = False):
    """Generates a QR code from the given text or URL."""
    qr = qrcode.make(text)

    # Creates an in-memory buffer
    img_io = io.BytesIO()

    # Save the QR code to the buffer in PNG format
    qr.save(img_io, format="PNG")

    # Move the pointer back to the start of the buffer
    img_io.seek(0)

    if download:
        return Response(
            content=img_io.getvalue(),
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename=qr_code.png",
                     "Content-Length": str(len(img_io.getvalue()))
                     }
        )

    # Return the image as a response without saving it
    return StreamingResponse(img_io, media_type="image/png")

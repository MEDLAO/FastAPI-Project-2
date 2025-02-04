import io
import qrcode
from fastapi import FastAPI, Query, Response, Request
from fastapi.responses import JSONResponse, StreamingResponse


app = FastAPI()


# @app.middleware("http")
# async def validate_rapidapi_request(request: Request, call_next):
#     rapidapi_key = request.headers.get("X-RapidAPI-Key")
#
#     if not rapidapi_key:
#         return JSONResponse(status_code=403, content={"error": "Access restricted to RapidAPI users."})
#
#     return await call_next(request)


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
            headers={"Content-Disposition": f"attachment; filename=qr_code.png"}
        )

    # Return the image as a response without saving it
    return StreamingResponse(img_io, media_type="image/png")

import io
import qrcode
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse


app = FastAPI()


@app.get("/generate_qr/")
def generate_qr(text: str = Query(..., description="Text or URL to encode in QR Code")):
    """Generates a QR code from the given text or URL."""
    qr = qrcode.make(text)

    # Creates an in-memory buffer
    img_io = io.BytesIO()

    # Save the QR code to the buffer in PNG format
    qr.save(img_io, format="PNG")

    # Move the pointer back to the start of the buffer
    img_io.seek(0)

    # Return the image as a response without saving it
    return StreamingResponse(img_io, media_type="image/png")

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import string
import random

app = FastAPI()

# temp storage
url_db = {}


class URLRequest(BaseModel):
    long_url: str


def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


@app.post("/shorten")
def shorten_url(request: URLRequest):
    short_code = generate_short_code()
    url_db[short_code] = request.long_url
    return {"short_url": f"http://localhost:8000/{short_code}"}


@app.get("/{short_code}")
def redirect_url(short_code: str):
    if short_code in url_db:
        return RedirectResponse(url=url_db[short_code])
    raise HTTPException(status_code=404, detail="URL not found")

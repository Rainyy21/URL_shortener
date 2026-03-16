from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse

# redis
from cache.redis_client import redis_client

# the sqlalchemy
from sqlalchemy.orm import Session
import string
import random

# the database
from db.database import SessionLocal, engine
from db import models, crud, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


@app.post("/shorten", response_model=schemas.URLResponse)
def shorten_url(request: schemas.URLCreate, db: Session = Depends(get_db)):
    short_code = generate_short_code()

    crud.create_url(db, short_code, request.long_url)

    # set it in cache for a hour
    redis_client.set(short_code, request.long_url, ex=3600)

    return {"short_url": f"http://localhost:8000/{short_code}"}


@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    # check the redis
    check_url = redis_client.get(short_code)

    if check_url:
        return RedirectResponse(url=check_url)

    # get url from the db
    db_url = crud.get_url(db, short_code)
    # throw a error if url not in db
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")

    redis_client.set(short_code, db_url.long_url)
    return RedirectResponse(url=db_url.long_url)

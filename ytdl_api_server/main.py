from db import DB

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

DBH = DB()


class UrlModel(BaseModel):
    url: str


@app.get("/urls/pending")
def pending():
    return DBH.get_pending_urls()


@app.post("/urls/add")
def add(url: UrlModel):
    DBH.add_url(url.url)

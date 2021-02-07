from db import DB

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

DBH = DB()


class UrlModel(BaseModel):
    url: str


@app.get("/urls/pending")
def pending():
    '''Return IDs and URLs of yet-to-be downloaded URLs
    '''

    return DBH.get_pending_urls()


@app.post("/urls/add")
def add(url: UrlModel):
    ''' Add a new URL for downloading
    '''

    DBH.add_url(url.url)

from db import DB

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

DBH = DB()


class UrlModel(BaseModel):
    url: str

class UrlIdModel(BaseModel):
    id: int


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

@app.put("/urls/downloaded")
def mark_downloaded(urlid: UrlIdModel):
    ''' Update a URL ID as downloaded
    '''

    DBH.mark_url_downloaded(urlid.id)

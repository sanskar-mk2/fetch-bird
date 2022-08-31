from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from os import walk
from Integration import fetch_tweet
from Tweet import Tweet

app = FastAPI(docs_url="/")


@app.get("/tweet")
def get_tweet(url: str, force: bool = False):
    return fetch_tweet(url, force)


@app.get("/images/{folder}/{file}")
def get_image(folder: str, file: str):
    walker = walk("./images")
    _, folders, _ = next(walker)
    if folder not in folders:
        raise HTTPException(400, "Folder not found")

    _, _, files = next(walk(f"./images/{folder}"))
    if file not in files:
        raise HTTPException(400, "File not found in folder")
    return FileResponse(f"./images/{folder}/{file}")

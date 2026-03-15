from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pyrogram import Client
import os

app = FastAPI()

api_id = int(os.getenv("37842280"))
api_hash = os.getenv("2072f15622817236d2ed00bcc4055994")
bot_token = os.getenv("8747819132:AAEgvpcj9wkcSVGXYLvfoAiKFa8ZsRiA-l8")

tg = Client("streambot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_event("startup")
async def startup():
    await tg.start()

@app.on_event("shutdown")
async def shutdown():
    await tg.stop()

@app.get("/stream/{file_id}")
async def stream(file_id: str):

    file_path = await tg.download_media(file_id)

    def iterfile():
        with open(file_path, "rb") as f:
            while chunk := f.read(1024 * 1024):
                yield chunk

    return StreamingResponse(iterfile(), media_type="video/mp4")


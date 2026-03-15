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

    async def generator():
        async for chunk in tg.stream_media(file_id):
            yield chunk

    return StreamingResponse(generator(), media_type="video/mp4")

active_connections = 0
MAX_USERS = 10

@app.get("/stream/{file_id}")
async def stream_video(file_id: str):

    global active_connections

    if active_connections >= MAX_USERS:
        raise HTTPException(429,"Server full")

    active_connections += 1

    async def generator():
        try:
            async for chunk in tg.stream_media(file_id):
                yield chunk
        finally:
            global active_connections
            active_connections -= 1

    return StreamingResponse(generator(), media_type="video/mp4")

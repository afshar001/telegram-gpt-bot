from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from database import database, messages
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/", response_class=HTMLResponse)
async def read_messages():
    query = messages.select().order_by(messages.c.timestamp.desc())
    rows = await database.fetch_all(query)
    html = "<h1>پیام‌های کاربران</h1><ul>"
    for row in rows:
        html += f"<li><b>{row['username'] or 'ناشناس'}:</b> {row['text']} <i>({row['timestamp']})</i></li>"
    html += "</ul>"
    return html

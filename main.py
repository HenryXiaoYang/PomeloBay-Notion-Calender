from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

from get_calender import get_calendar

with open("calender_template.html", "r") as f:
    calender_template = f.read()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    FastAPICache.init(InMemoryBackend())
    yield
    await FastAPICache.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@cache(expire=86400)
async def cache_calender():
    calender_html = await get_calendar(calender_template)
    return calender_html


@app.get("/calender")
async def calender():
    calender_html = await cache_calender()
    return HTMLResponse(content=calender_html)

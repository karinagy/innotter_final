from fastapi import FastAPI
from consumer import consume
from router import router

app = FastAPI()
app.include_router(router)


@app.on_event('startup')
async def startup():
    await consume()
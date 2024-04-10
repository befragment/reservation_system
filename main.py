from fastapi import FastAPI
import uvicorn

from internal import admin
from routers import rent


app = FastAPI(
    title="VesnaBackEnd"
)

app.include_router(rent.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return { "hello": "rootie" }



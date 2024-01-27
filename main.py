from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scripts.core.services import router


class FastAPIConfig(BaseModel):
    title: str = "SKA Essentials API"
    description: str = "API for SKA Essentials"
    version: str = "0.1.0"
    root_path: str = "/proto1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"


app = FastAPI(**FastAPIConfig().model_dump())
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://be.faizanazim11.codes",
        "http://be.faizanazim11.codes",
        "http://fe.faizanazim11.codes",
        "https://fe.faizanazim11.codes",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.include_router(router)

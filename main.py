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


app = FastAPI(**FastAPIConfig().model_dump())
app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:5173", "be.faizanazim11.codes"], allow_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"], allow_headers=["Access-Control-Allow-Headers", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin'], allow_credentials=True
)
app.include_router(router)

from fastapi import FastAPI
from app import router_ai
from .kobert import init_kobert
from fastapi.middleware.cors import CORSMiddleware

init_kobert()

app = FastAPI(title="졸업프로젝트 AI 모듈 API", description="AIHub API 데이터를 AI모듈 전처리하여 제공하는 API")

app.include_router(router_ai, tags=["AI"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

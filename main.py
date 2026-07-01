import logging
from fastapi import FastAPI, Request

#새로 만든 ai_router를 불러옵니다
from routers import ai_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI 카피라이터 서버",
    description="Gemini Vision AI를 이용한 인스타 해시태그 및 캡션 자동 생성 API",
    version="1.0.0"
)

# 라우터 등록: 외부에서 /api/v1/generate-keywords 주소로 접속할 수 있게 연결합니다.
app.include_router(ai_router.router, prefix="/api/v1", tags=["AI_Generation"])

@app.get("/")
def health_check(request: Request):
    """서버가 죽지 않고 잘 살아있는지 확인하는 창구입니다."""
    logger.info(f"Health check called from {request.client.host}")
    return {"status": "ok", "message": "AI Server is running perfectly!"}
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

# 💡 옆 폴더(services)에 있는 질문자님의 AI 함수를 불러옵니다.
from services.AI_keyword import extract_keywords_from_multiple_images
# from services.AI_recommender import generate_scripts_from_multiple_images # (필요시 주석 해제)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate-keywords")
async def generate_keywords(files: List[UploadFile] = File(...)):
    """
    유저가 업로드한 여러 장의 사진을 분석하여 인스타 감성 해시태그를 즉시 반환합니다.
    """
    # 1. 파일 검증 (모든 파일이 이미지인지 확인)
    for file in files:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")

    try:
        # 2. 비동기로 파일을 읽어서 바이트(bytes) 리스트로 변환
        image_bytes_list = []
        for file in files:
            contents = await file.read()
            image_bytes_list.append(contents)
            
        # 3. 질문자님의 AI 서비스 호출 (Gemini 엔진 가동)
        logger.info(f"{len(files)}장의 이미지 분석을 시작합니다...")
        ai_tags = extract_keywords_from_multiple_images(image_bytes_list)
        
        # 4. 결과 반환 (콜백 없이 곧바로 데이터 던져주기)
        logger.info("✅ AI 분석 성공!")
        return {
            "success": True,
            "tags": ai_tags
        }
        
    except Exception as e:
        # 구글 서버 과부하(503, 429) 등의 에러가 발생하면 여기서 부드럽게 처리됩니다.
        logger.error(f"AI 처리 중 오류가 발생했습니다: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI가 현재 너무 바쁩니다! 잠시 후 다시 시도해주세요. (사유: {str(e)})")
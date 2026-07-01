import os
import json
from google import genai
from google.genai import types 
from pydantic import BaseModel
from dotenv import load_dotenv

# 1. API 키 셋업
load_dotenv()
client = genai.Client(api_key=os.environ.get("API_KEY"))

# 2. 백엔드와 약속한 데이터 출력 규격 (JSON)
class RecommendationResponse(BaseModel):
    similar_activity: str
    new_activity: str

# ==========================================
# 🛠️ [메인 엔진] 백엔드가 호출해서 사용할 순수 함수
# ==========================================
def get_activity_recommendation(room_context: str, user_history: str) -> dict:
    """
    백엔드로부터 방 정보와 유저 과거 기록을 텍스트로 받아,
    투트랙(유사 취향, 분위기 환기) 추천 결과를 딕셔너리로 반환합니다.
    """
    
    sys_instruct = f"""
    너는 인스타그램 릴스와 트렌드에 극도로 민감한 20대 대학생 맞춤형 큐레이터야.
    
    [분석할 데이터]
    - 현재 소속된 방의 성격: {room_context}
    - 이 유저의 과거 활동 기록(주로 쓴 태그들): {user_history}
    
    위 데이터를 바탕으로, 이 방의 주제에 맞는 다음 활동을 2가지 방향으로 제안해 줘.
    1. similar_activity (취향 연장선): 과거 기록의 감성과 비슷한 분위기나 장소
    2. new_activity (분위기 환기): 기존 활동과 반대되거나 완전 색다른 자극을 주는 추천
    
    🚨 [절대 금지 규칙]
    - '청춘', '낭만', '추억', '힐링', '우정' 등 뻔하고 올드한 싸이월드 감성 단어 절대 금지.
    - 너무 길고 딱딱한 문장 금지.
    
    ✨ [추구하는 요즘 감성]
    - 친구에게 DM이나 카톡으로 무심하게 툭 추천하듯, 담백하고 센스 있는 말투.
    - 각 옵션당 핵심만 2~3줄로 명확하게 작성.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="위의 방 성격과 유저 기록을 분석해서 맞춤형 활동 2가지를 추천해 줘.",
        config=types.GenerateContentConfig(
            system_instruction=sys_instruct,
            response_mime_type="application/json",
            response_schema=RecommendationResponse
        )
    )
    
    return json.loads(response.text)

# ==========================================
# 💻 로컬 자동화 테스트 실행부 (백엔드 연동 시 무시됨)
# ==========================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 AI 맞춤형 추천 기능 로컬 테스트")
    print("="*50 + "\n")

    # [테스트용 더미 데이터 세팅]
    # 💡 나중에 백엔드가 DB에서 이 데이터를 뽑아서 함수에 넣어줄 것입니다.
    test_room = "방 이름: 기분 전환 / 카테고리: 맛집, 공원, 액비티비, 야외"
    test_history = """
    1. [5일 전] 주 사용 태그: #한강공원, #자전거, #치맥, #야외활동
    2. [2주 전] 주 사용 태그: #보드게임, #실내놀거리, #승부욕, #루미큐브
    3. [3일 전] 주 사용 태그: #방탈출, #머리쓰기, #힌트요정, #실내액티비티"""

    print("📥 [입력된 맥락 데이터]")
    print(f" - 방 성격: {test_room}")
    print(f" - 유저 기록: {test_history}\n")
    print("⏳ AI가 데이터를 융합하여 솔루션을 도출하는 중...\n")

    # 💡 메인 엔진 함수 실행
    result = get_activity_recommendation(test_room, test_history)

    print("✨ [다음에 이런 활동은 어떠세요?]")
    print("-" * 50)
    print("👉 [옵션 A: 취향 연장선]")
    print(result['similar_activity'])
    print("\n👉 [옵션 B: 분위기 환기]")
    print(result['new_activity'])
    print("-" * 50)
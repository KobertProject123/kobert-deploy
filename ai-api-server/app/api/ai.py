from fastapi import APIRouter
from ..model import ConversationResponse
from ..kobert import get_pair_affinity_score
import math
import httpx

router = APIRouter()

@router.get("/conversation/ai", response_model=ConversationResponse)
async def get_conversation_with_intimacy(conversation_id: str):
    client = httpx.AsyncClient(timeout=230.0)
    
    raw_conversation = await get_raw_conversation(client, conversation_id)
    response = decorate_conversation_data(raw_conversation)

    return response

def decorate_conversation_data(data):
    # 데이터 복사 (원본 데이터 보존)
    decorated_data = data.copy()
    decorated_data['utterances'] = []
    
    utterances = data['utterances']
    
    # 각 utterance에 forward와 backward 필드 초기화
    for i, utterance in enumerate(utterances):
        decorated_utterance = utterance.copy()
        decorated_utterance['forward_intimacy'] = -1
        decorated_utterance['backward_intimacy'] = -1
        decorated_data['utterances'].append(decorated_utterance)
    
    # 연속된 utterance 쌍에 대해 function 실행
    for i in range(len(utterances) - 1):
        text1 = utterances[i]['text']
        text2 = utterances[i + 1]['text']
        
        # function 호출
        score = get_pair_affinity_score(text1, text2)
        # score = math.log(score, 2)

        # 결과값을 해당 위치에 저장
        decorated_data['utterances'][i]['backward_intimacy'] = score      # i번째의 backward
        decorated_data['utterances'][i + 1]['forward_intimacy'] = score   # i+1번째의 forward
    
    return decorated_data



def get_test_conversation(client, conversation_id):
    data = {
  "conversation_id": "BP2200905",
  "utterances": [
    {
      "utterance_id": "BP2200905.1",
      "persona_id": 2,
      "text": "요즘 매일 헬스장에 줄곧 도장을 찍고 있어요. 헬스가 이렇게 재미있는지 몰랐어요.",
      "terminate": False
    },
    {
      "utterance_id": "BP2200905.2",
      "persona_id": 135,
      "text": "저도 헬스 다녀요! 집 근처에 여성 전용 헬스장이 생겨서요.",
      "terminate": False
    },
    {
      "utterance_id": "BP2200905.3",
      "persona_id": 2,
      "text": "22년 살면서 처음 헬스를 해보는건데 저한테 딱 맞는 것 같아요. 그래서 요즘 관련 물품을 많이 사고 있어요.",
      "terminate": False
    },
    {
      "utterance_id": "BP2200905.4",
      "persona_id": 135,
      "text": "저는 아직 아무것도 안 샀어요. 필요한 게 많은가요?.",
      "terminate": False
    },
    {
      "utterance_id": "BP2200905.5",
      "persona_id": 2,
      "text": "저는 그런것 같아요. 신발, 양말처럼 운동에 맞는 장비가 중요하더라고요.",
      "terminate": True
    }
  ]
}
    return data

async def get_raw_conversation(client, conversation_id):
    url = f"http://localhost:5000/api/conversation/{conversation_id}"

    response = await client.get(url)
    response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        
    return response.json()

def decorate_with_intimacy(raw_conversation):
    return
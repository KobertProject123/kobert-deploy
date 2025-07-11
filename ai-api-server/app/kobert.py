import torch
from transformers import BertTokenizer, BertForSequenceClassification

tokenizer = None
model = None

def init_kobert():
    global tokenizer
    global model
    
    # KoBERT 감정 분류 모델 로드 (긍정/중립/부정)
    MODEL_NAME = "beomi/kcbert-base"
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    model = BertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3)
    model.eval()

# “A → B” 쌍을 입력으로 학습된 KoBERT에 넘겨, '긍정 확률'만 뽑는 함수
def get_pair_affinity_score(text_A, text_B):
    # [CLS] A 발화 [SEP] B 응답
    encoded = tokenizer(
        text_A,
        text_B,
        return_tensors="pt",
        truncation=True,
        padding=True
    )
    with torch.no_grad():
        outputs = model(**encoded)
    probs = torch.softmax(outputs.logits, dim=1).squeeze().tolist()
    # 세 레이블 중 “긍정” 확률을 호감도로 간주
    return probs[2]

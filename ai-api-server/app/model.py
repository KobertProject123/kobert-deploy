from pydantic import BaseModel

class Utterance(BaseModel):
    utterance_id: str
    persona_id: int
    text: str
    terminate: bool
    forward_intimacy: float
    backward_intimacy: float

class ConversationResponse(BaseModel):
    utterances: list[Utterance]


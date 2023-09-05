 from typing import Optional
 from pydantic import BaseModel

 # Request Body로 받을 데이터 정의 : 지금은 사용하지 않지만, 추후 수정 후 사용 예정
 class ChatbotMessage(BaseModel):
     name: Optional[str] = None  # optional value
     chatbot_answer: str         # required value

     # ChatbotMessage 모델 항목을 자동으로 스키마로 매핑
     class Config:
         orm_mode = True

from fastapi import APIRouter, Depends, Request
import requests

#import openai
# from schema.chatbot_schema import ChatbotMessage

# Creating a Router Object
router = APIRouter()

# Write the flask app's ngrok url address here
flask_ngrok_url = "http://c2cd-34-32-225-166.ngrok-free.app"  # Writing example

# 연결 테스트4 : 프론트에서 보낸 요청 flask로 보내고 chatGPT 답장 받아서 프론트로 보내기
@router.post("/chatbot")
async def test_route3(request: Request):
    data = await request.json()
    response = requests.post(flask_ngrok_url + "/chatbot", json=data)
    text = response.json()
    return text

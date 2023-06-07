from fastapi import APIRouter, Depends
import requests
# from schema.chatbot_schema import ChatbotMessage

# Creating a Router Object
router = APIRouter()


# Write the flask app's ngrok url address here
flask_ngrok_url = "http://ff9f-34-83-215-199.ngrok-free.app"  # Writing example

# Data to be entered from the client (for testing)
test_message = {
    "message": "hello"
}

# router list
@router.get("/intro")
def chatbot_intro():
    return {"message": "Welcome to Odego."}

@router.post("/chatbot")
async def test_route3():
    response = requests.post(flask_ngrok_url + "/chatbot", json=test_message)
    return response.json()

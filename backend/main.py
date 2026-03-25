
import asyncio
from fastapi import FastAPI, HTTPException, File, UploadFile
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
import os

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="Mirror, Mirror API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for storing selfies
# Ensure the selfies directory exists and is writable
SELFIE_DIR = os.path.join(os.path.dirname(__file__), "selfies")
os.makedirs(SELFIE_DIR, exist_ok=True)


# Initialize AzureChatOpenAI from environment variables
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", "grace-first-project-gpt-4"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
)

# Define the UserInput class
class UserInput(BaseModel):
    user_text: str

# Define the ConversationState class
class ConversationState(BaseModel):
    step: int = 0
    responses: list[str] = []
    
conversation_state = ConversationState()

# Generate affirmation after chatting with users
@app.post("/generate-affirmation")
async def generate_affirmation(input: UserInput):
    try:
        # conversation_state.responses.append(input.user_text)

        if conversation_state.step == 0:
            conversation_state.responses.append(input.user_text)
            # Step 0: Greet the user and ask how they feel
            prompt = ChatPromptTemplate(
                [
                    ("system", "You are an AI-powered interactive mirror called **Mirror, Mirror**. Your purpose is to help users start their day with a positive mindset. You act as a friendly, supportive, and empathetic companion. You greet users with questions about their current feelings."),
                    ("user", conversation_state.responses[0]),
                ]
            )
            response = llm.invoke(prompt.format(user_input=input.user_text))
            conversation_state.step += 1
            return { "message": response.content}
        elif conversation_state.step == 1:
            conversation_state.responses.append(input.user_text)
            # Step 1: Ask a follow-up question based on the user's response
            await asyncio.sleep(2)  # Simulate a delay
            conversation_state.step += 1
            return {"message": "Thank you for sharing. Can you tell me more about what's on your mind?"}
        elif conversation_state.step == 2:
            conversation_state.responses.append(input.user_text)
            # Step 2: Generate the affirmation based on the conversation
            prompt = ChatPromptTemplate(
                [
                    ("system", "You are an AI-powered interactive mirror called **Mirror, Mirror**. Your purpose is to help users start their day with a positive mindset. You act as a friendly, supportive, and empathetic companion. You give users positive affirmations based on their current feelings."),
                    ("user", conversation_state.responses[0]),
                    ("user", conversation_state.responses[1]),
                    ("user", conversation_state.responses[2])
                ]
            )
            response = llm.invoke(prompt.format(user_input=input.user_text))
            conversation_state.step += 1
            return { "message": f"{response.content} Would you like to take a selfie today?"}
        elif conversation_state.step == 3:
            # Step 3: Ask if the user wants to take a selfie
            if "yes" in input.user_text.lower():
                await asyncio.sleep(2)  # Simulate a delay
                conversation_state.step = 0  # Reset the conversation state
                return {"message": "Great! Let's take a selfie.", "selfie_url": "/take-selfie"}
            else:
                await asyncio.sleep(2)  # Simulate a delay
                conversation_state.step = 0  # Reset the conversation state
                return {"message": "No problem! Have a wonderful day!"}
    except Exception as e:
        print (f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to Mirror, Mirror API"}

# Endpoint to handle selfie functionality
@app.post("/take-selfie")
async def take_selfie(photo: UploadFile = File(...)):
    try:
        # Sanitize filename to prevent directory traversal
        safe_name = os.path.basename(photo.filename or "selfie.png")
        filename = f"{uuid4().hex}_{safe_name}"
        filepath = os.path.join(SELFIE_DIR, filename)

        # Save the photo to the selfies directory
        content = await photo.read()
        with open(filepath, "wb") as f:
            f.write(content)

        return {"message": "Selfie saved successfully!", "file_id": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving selfie: {str(e)}")

    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
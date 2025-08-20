
import asyncio
from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, status
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import timedelta
from sqlalchemy.orm import Session
import os

# Import our new modules
from database import create_tables, get_db, User, Selfie
from auth import (
    authenticate_user, 
    create_access_token, 
    get_current_user, 
    get_password_hash,
    get_user_by_username,
    get_user_by_email,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from models import UserCreate, UserLogin, UserResponse, Token, SelfieResponse

# Create database tables on startup
create_tables()

# Load environment variables from .env file
from dotenv import load_dotenv
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

# Authentication endpoints
@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token."""
    authenticated_user = authenticate_user(db, user.username, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": authenticated_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user


@app.get("/my-selfies", response_model=list[SelfieResponse])
async def get_my_selfies(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user's selfies."""
    selfies = db.query(Selfie).filter(Selfie.user_id == current_user.id).all()
    return selfies

# Directory for storing selfies - kept for backward compatibility
SELFIE_DIR = "selfies"
os.makedirs(SELFIE_DIR, exist_ok=True)

# Temporarily commented out langchain functionality due to dependency issues
# TODO: Restore when langchain dependencies are available
# # Initialize AzureChatOpenAI
# llm = AzureChatOpenAI(
#     azure_deployment="grace-first-project-gpt-4",
#     api_version="2024-10-21",
# )

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
        # Temporarily simplified response without langchain
        # TODO: Restore full AI functionality when langchain is available
        
        if conversation_state.step == 0:
            conversation_state.responses.append(input.user_text)
            conversation_state.step += 1
            return {"message": "Hello! I'm Mirror, Mirror. How are you feeling today?"}
        elif conversation_state.step == 1:
            conversation_state.responses.append(input.user_text)
            await asyncio.sleep(2)
            conversation_state.step += 1
            return {"message": "Thank you for sharing. Can you tell me more about what's on your mind?"}
        elif conversation_state.step == 2:
            conversation_state.responses.append(input.user_text)
            conversation_state.step += 1
            return {"message": "You are wonderful and capable! Today is full of possibilities. Would you like to take a selfie today?"}
        elif conversation_state.step == 3:
            if "yes" in input.user_text.lower():
                await asyncio.sleep(2)
                conversation_state.step = 0
                return {"message": "Great! Let's take a selfie.", "selfie_url": "/take-selfie"}
            else:
                await asyncio.sleep(2)
                conversation_state.step = 0
                return {"message": "No problem! Have a wonderful day!"}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to Mirror, Mirror API"}

# Endpoint to handle selfie functionality
@app.post("/take-selfie", response_model=SelfieResponse)
async def take_selfie(
    photo: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Generate a unique filename
        filename = f"{uuid4().hex}_{photo.filename}"
        
        # Read the photo data
        photo_data = await photo.read()
        
        # Save to database instead of filesystem
        db_selfie = Selfie(
            filename=filename,
            original_filename=photo.filename,
            file_data=photo_data,
            user_id=current_user.id
        )
        db.add(db_selfie)
        db.commit()
        db.refresh(db_selfie)
        
        # Also save to filesystem for backward compatibility (optional)
        filepath = os.path.join(SELFIE_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(photo_data)

        return db_selfie
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving selfie: {str(e)}")


# Endpoint to retrieve a selfie image
@app.get("/selfie/{selfie_id}")
async def get_selfie(
    selfie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a selfie image by ID (only owner can access)."""
    selfie = db.query(Selfie).filter(
        Selfie.id == selfie_id,
        Selfie.user_id == current_user.id
    ).first()
    
    if not selfie:
        raise HTTPException(status_code=404, detail="Selfie not found")
    
    from fastapi.responses import Response
    return Response(
        content=selfie.file_data,
        media_type="image/jpeg",
        headers={"Content-Disposition": f"inline; filename={selfie.original_filename}"}
    )

    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
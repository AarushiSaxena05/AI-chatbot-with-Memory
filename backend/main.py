from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models, schemas
from memory import (
    save_message,
    get_recent_messages,
    get_user_profile,
    update_user_profile,
    extract_user_info
)
from ai_service import generate_response

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/user", response_model=schemas.UserResponse)
def create_or_update_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    updated_user = update_user_profile(db, user_id=1, data=user.dict())
    return updated_user


@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    messages = get_recent_messages(db, user_id=1)
    return messages


@app.post("/chat")
def chat(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    user_id = message.user_id

    # Save user message
    save_message(db, user_id, "user", message.content)

    # Extract info
    extracted = extract_user_info(message.content)
    if extracted:
        update_user_profile(db, user_id, extracted)

    # Fetch memory
    history = get_recent_messages(db, user_id)
    user_profile = get_user_profile(db, user_id)

    # Generate response
    ai_response = generate_response(message.content, user_profile, history)

    # Save AI response
    save_message(db, user_id, "assistant", ai_response)

    return {"response": ai_response}

@app.get("/")
def root():
    return {"message": "Chatbot API is running 🚀"}
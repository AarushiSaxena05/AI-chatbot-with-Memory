from sqlalchemy.orm import Session
from models import Message, User

MAX_HISTORY = 15


def save_message(db: Session, user_id: int, role: str, content: str):
    message = Message(user_id=user_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_recent_messages(db: Session, user_id: int):
    messages = (
        db.query(Message)
        .filter(Message.user_id == user_id)
        .order_by(Message.timestamp.desc())
        .limit(MAX_HISTORY)
        .all()
    )
    return list(reversed(messages))


def get_user_profile(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user_profile(db: Session, user_id: int, data: dict):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        user = User(id=user_id)

    for key, value in data.items():
        if value:
            setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Basic keyword extraction
def extract_user_info(text: str):
    text = text.lower()

    data = {}

    if "my name is" in text:
        data["name"] = text.split("my name is")[-1].strip().split(" ")[0]

    if "i like" in text:
        data["interests"] = text.split("i like")[-1].strip()

    if "i am learning" in text:
        data["skills"] = text.split("i am learning")[-1].strip()

    return data
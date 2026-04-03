"""
Telegram Auth Router - CRM user yaratish yoki olish
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class TelegramAuthRequest(BaseModel):
    """Telegram auth request body."""
    telegram_id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None


class CRMUserResponse(BaseModel):
    """CRM user response."""
    id: int
    telegram_id: str
    first_name: str
    last_name: str | None = None
    username: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


# In-memory user storage (databasaga o'tish kerak bo'ladi)
_users_db = {}
_next_id = 1


@router.post("/telegram", response_model=CRMUserResponse)
async def auth_telegram(request: TelegramAuthRequest):
    """
    Telegram user bilan autentifikatsiya.
    
    - User mavjud bo'lsa: qaytaradi
    - User mavjud bo'lmasa: yangi yaratadi
    """
    telegram_id_str = str(request.telegram_id)
    
    # User mavjudligini tekshirish
    if telegram_id_str in _users_db:
        user = _users_db[telegram_id_str]
        print(f"[auth] Mavjud user topildi: {user['first_name']} (ID: {telegram_id_str})")
        return CRMUserResponse(**user)
    
    # Yangi user yaratish
    global _next_id
    from datetime import datetime
    
    now = datetime.utcnow().isoformat()
    new_user = {
        "id": _next_id,
        "telegram_id": telegram_id_str,
        "first_name": request.first_name,
        "last_name": request.last_name,
        "username": request.username,
        "created_at": now,
        "updated_at": now,
    }
    
    _users_db[telegram_id_str] = new_user
    _next_id += 1
    
    print(f"[auth] Yangi user yaratildi: {new_user['first_name']} (ID: {telegram_id_str})")
    return CRMUserResponse(**new_user)


@router.get("/users/{telegram_id}")
async def get_user(telegram_id: str):
    """Telegram ID bo'yicha user olish (test uchun)."""
    if telegram_id not in _users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return CRMUserResponse(**_users_db[telegram_id])


@router.get("/users")
async def list_users():
    """Barcha userlarni olish (test uchun)."""
    return [CRMUserResponse(**user) for user in _users_db.values()]

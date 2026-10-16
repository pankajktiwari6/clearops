from itertools import count

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI(title="user-service", version="0.1.0")

_users: dict[int, dict] = {}
_ids = count(1)


class UserIn(BaseModel):
    name: str
    email: EmailStr


class User(UserIn):
    id: int


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/users", response_model=User, status_code=201)
def create_user(body: UserIn) -> dict:
    user = {"id": next(_ids), **body.model_dump()}
    _users[user["id"]] = user
    return user


@app.get("/users", response_model=list[User])
def list_users() -> list[dict]:
    return list(_users.values())


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int) -> dict:
    if user_id not in _users:
        raise HTTPException(404, "User not found")
    return _users[user_id]

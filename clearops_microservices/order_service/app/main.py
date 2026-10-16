import os
from itertools import count

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8001")

app = FastAPI(title="order-service", version="0.1.0")

_orders: dict[int, dict] = {}
_ids = count(1)


class OrderIn(BaseModel):
    user_id: int
    item: str
    quantity: int = Field(gt=0)


class Order(OrderIn):
    id: int


def user_exists(user_id: int) -> bool:
    """Ask the user service whether the user exists."""
    try:
        r = httpx.get(f"{USER_SERVICE_URL}/users/{user_id}", timeout=5)
    except httpx.HTTPError:
        raise HTTPException(503, "User service unavailable")
    return r.status_code == 200


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/orders", response_model=Order, status_code=201)
def create_order(body: OrderIn) -> dict:
    if not user_exists(body.user_id):
        raise HTTPException(404, "User not found")
    order = {"id": next(_ids), **body.model_dump()}
    _orders[order["id"]] = order
    return order


@app.get("/orders", response_model=list[Order])
def list_orders(user_id: int | None = None) -> list[dict]:
    return [o for o in _orders.values() if user_id in (None, o["user_id"])]


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int) -> dict:
    if order_id not in _orders:
        raise HTTPException(404, "Order not found")
    return _orders[order_id]

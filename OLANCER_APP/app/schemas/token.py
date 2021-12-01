from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    id: int
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None

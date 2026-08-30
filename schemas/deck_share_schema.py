from pydantic import BaseModel


class DeckShareCreate(BaseModel):
    user_id: int
    permission: str = "VIEW"


class DeckShareResponse(BaseModel):
    id: int
    user_id: int
    deck_id: int
    permission: str

    class Config:
        from_attributes = True

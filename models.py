from pydantic import BaseModel


class Review(BaseModel):
    id: int
    user_id: str
    rating: int
    review: str


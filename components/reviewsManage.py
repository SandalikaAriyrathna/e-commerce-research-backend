from fastapi import APIRouter, HTTPException
from typing import List
from models import Review

router = APIRouter()


reviews = []

@router.post("/reviews/", response_model=Review)
def add_review(review: Review):
    reviews.append(review)
    return review

@router.get("/reviews/", response_model=List[Review])
def get_reviews():
    return reviews

@router.get("/reviews/{review_id}", response_model=Review)
def get_review(review_id: int):
    for review in reviews:
        if review.id == review_id:
            return review
    raise HTTPException(status_code=404, detail="Review not found")

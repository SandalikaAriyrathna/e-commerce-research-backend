from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from components.reviewsManage import router as reviews_router

app = FastAPI(title="Reviews Summary", version="1.0")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Security and authentication setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "admin": {
        "username": "sandali",
        "full_name": "sandali",
        "email": "sandali@gmail.com",
        "hashed_password": "sandali123", 
        "disabled": False,
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users", response_model=User)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    user = get_user(fake_users_db, token)
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid authentication credentials")
    return user

# Include routers from different components
app.include_router(reviews_router, prefix="/api/v1/reviews", tags=["Reviews"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome"}
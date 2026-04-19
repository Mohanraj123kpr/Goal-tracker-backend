import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from database import engine, get_db, Base
import models, crud
from auth import verify_password, create_access_token, get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Goal Tracker API")

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:4200").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Auth ──────────────────────────────────────────────────────

@app.post("/auth/register", response_model=models.TokenResponse, status_code=201)
def register(user: models.UserRegister, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.create_user(db, user)
    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer", "user": db_user}


@app.post("/auth/login", response_model=models.TokenResponse)
def login(credentials: models.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, credentials.email)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": user}


@app.get("/auth/me", response_model=models.UserResponse)
def me(current_user: models.UserDB = Depends(get_current_user)):
    return current_user


# ── Goals ─────────────────────────────────────────────────────

@app.get("/goals", response_model=List[models.GoalResponse])
def list_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.UserDB = Depends(get_current_user)):
    return crud.get_goals(db, user_id=current_user.id, skip=skip, limit=limit)


@app.get("/goals/{goal_id}", response_model=models.GoalResponse)
def get_goal(goal_id: int, db: Session = Depends(get_db), current_user: models.UserDB = Depends(get_current_user)):
    goal = crud.get_goal(db, goal_id, user_id=current_user.id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@app.post("/goals", response_model=models.GoalResponse, status_code=201)
def create_goal(goal: models.GoalCreate, db: Session = Depends(get_db), current_user: models.UserDB = Depends(get_current_user)):
    return crud.create_goal(db, goal, user_id=current_user.id)


@app.patch("/goals/{goal_id}", response_model=models.GoalResponse)
def update_goal(goal_id: int, goal: models.GoalUpdate, db: Session = Depends(get_db), current_user: models.UserDB = Depends(get_current_user)):
    updated = crud.update_goal(db, goal_id, goal, user_id=current_user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Goal not found")
    return updated


@app.delete("/goals/{goal_id}", response_model=models.GoalResponse)
def delete_goal(goal_id: int, db: Session = Depends(get_db), current_user: models.UserDB = Depends(get_current_user)):
    deleted = crud.delete_goal(db, goal_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Goal not found")
    return deleted

# This is important for Vercel
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from database import engine, get_db, Base
import models, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Goal Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/goals", response_model=List[models.GoalResponse])
def list_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_goals(db, skip=skip, limit=limit)


@app.get("/goals/{goal_id}", response_model=models.GoalResponse)
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = crud.get_goal(db, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@app.post("/goals", response_model=models.GoalResponse, status_code=201)
def create_goal(goal: models.GoalCreate, db: Session = Depends(get_db)):
    return crud.create_goal(db, goal)


@app.patch("/goals/{goal_id}", response_model=models.GoalResponse)
def update_goal(goal_id: int, goal: models.GoalUpdate, db: Session = Depends(get_db)):
    updated = crud.update_goal(db, goal_id, goal)
    if not updated:
        raise HTTPException(status_code=404, detail="Goal not found")
    return updated


@app.delete("/goals/{goal_id}", response_model=models.GoalResponse)
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_goal(db, goal_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Goal not found")
    return deleted

from sqlalchemy.orm import Session
from models import GoalDB, GoalCreate, GoalUpdate


def get_goals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(GoalDB).offset(skip).limit(limit).all()

def get_goal(db: Session, goal_id: int):
    return db.query(GoalDB).filter(GoalDB.id == goal_id).first()

def create_goal(db: Session, goal: GoalCreate):
    db_goal = GoalDB(**goal.model_dump())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def update_goal(db: Session, goal_id: int, goal: GoalUpdate):
    db_goal = get_goal(db, goal_id)
    if not db_goal:
        return None
    for key, value in goal.model_dump(exclude_unset=True).items():
        setattr(db_goal, key, value)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def delete_goal(db: Session, goal_id: int):
    db_goal = get_goal(db, goal_id)
    if not db_goal:
        return None
    db.delete(db_goal)
    db.commit()
    return db_goal

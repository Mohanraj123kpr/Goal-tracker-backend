from sqlalchemy.orm import Session
from models import GoalDB, GoalCreate, GoalUpdate, UserDB, UserRegister
from auth import hash_password


# ── User CRUD ─────────────────────────────────────────────────

def get_user_by_email(db: Session, email: str):
    return db.query(UserDB).filter(UserDB.email == email).first()

def create_user(db: Session, user: UserRegister):
    db_user = UserDB(
        email=user.email,
        name=user.name,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ── Goal CRUD ─────────────────────────────────────────────────

def get_goals(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(GoalDB).filter(GoalDB.user_id == user_id).offset(skip).limit(limit).all()

def get_goal(db: Session, goal_id: int, user_id: int):
    return db.query(GoalDB).filter(GoalDB.id == goal_id, GoalDB.user_id == user_id).first()

def create_goal(db: Session, goal: GoalCreate, user_id: int):
    db_goal = GoalDB(**goal.model_dump(), user_id=user_id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def update_goal(db: Session, goal_id: int, goal: GoalUpdate, user_id: int):
    db_goal = get_goal(db, goal_id, user_id)
    if not db_goal:
        return None
    for key, value in goal.model_dump(exclude_unset=True).items():
        setattr(db_goal, key, value)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def delete_goal(db: Session, goal_id: int, user_id: int):
    db_goal = get_goal(db, goal_id, user_id)
    if not db_goal:
        return None
    db.delete(db_goal)
    db.commit()
    return db_goal

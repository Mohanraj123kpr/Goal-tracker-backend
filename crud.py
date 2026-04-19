from sqlalchemy.orm import Session
from models import GoalDB, GoalCreate, GoalUpdate, UserDB, UserRegister
from auth import hash_password
from datetime import date
from dateutil.relativedelta import relativedelta


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


# ── Recurrence helpers ────────────────────────────────────────

def _should_reset(goal: GoalDB, today: date) -> bool:
    """Return True if a recurring goal's period has passed and it should be reset."""
    if not goal.completed or goal.recurrence == "none":
        return False
    ref = goal.last_reset or goal.created_at.date()
    if goal.recurrence == "daily":
        return today > ref
    if goal.recurrence == "weekly":
        return (today - ref).days >= 7
    if goal.recurrence == "monthly":
        return today >= ref + relativedelta(months=1)
    return False

def _auto_reset(db: Session, goals: list[GoalDB]) -> list[GoalDB]:
    today = date.today()
    for g in goals:
        if _should_reset(g, today):
            g.completed = False
            g.last_reset = today
    db.commit()
    return goals


# ── Goal CRUD ─────────────────────────────────────────────────

def get_goals(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    goals = db.query(GoalDB).filter(GoalDB.user_id == user_id).offset(skip).limit(limit).all()
    return _auto_reset(db, goals)

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

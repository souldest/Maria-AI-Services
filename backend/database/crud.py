from sqlalchemy.orm import Session
from . import models


def create_user(db: Session, email: str, name: str):
    user = models.User(email=email, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_task(db: Session, user_id: int, task_name: str):
    task = models.Task(user_id=user_id, task_name=task_name)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def add_task_result(db: Session, task_id: int, text: str):
    result = models.TaskResult(task_id=task_id, result_text=text)
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def log_agent(db: Session, agent_name: str, input_text: str, output_text: str):
    log = models.AgentLog(
        agent_name=agent_name,
        input_text=input_text,
        output_text=output_text
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

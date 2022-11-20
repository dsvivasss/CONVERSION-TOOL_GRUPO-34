from sqlalchemy.orm import Session
from . import models, schemas

def create_file(db: Session, file: schemas.File):
    db.add(file)
    db.commit()
    db.refresh(file)
    return file

def get_files(db: Session):
    return db.query(models.File).all()

def get_file_user_id(db: Session, user_id: int):
    return db.query(models.File).filter_by(user = user_id).all()

def update_file_status_format(db: Session, new_status: str, new_format: str, id: int):
    file = get_file_id(db, id)
    file.status = new_status
    file.newFormat = new_format
    db.commit()
    db.refresh(file)
    return file
    
def update_file_status(db: Session, new_status: str, id: int):
    file = get_file_id(db, id)
    file.status = new_status
    db.commit()
    db.refresh(file)
    return file

def delete_file_id(db: Session, id: int):
    file = get_file_id(id)
    db.delete(file)
    db.commit()

def get_file_id(db:Session, id: int):
    return db.query(models.File).get(id)

def get_user_username(db: Session, username: str):
    return db.query(models.User).filter_by(username = username).first()

def get_user_email(db: Session, email: str):
    return db.query(models.User).filter_by(email = email).first()

def create_user(db: Session, user: models.User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
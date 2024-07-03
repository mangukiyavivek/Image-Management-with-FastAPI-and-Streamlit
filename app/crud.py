from sqlalchemy.orm import Session
from . import models, schemas

def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()

def create_image(db: Session, image: schemas.ImageCreate):
    db_image = models.Image(name=image.name, url=image.url, type=image.type)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def delete_image(db: Session, image_id: int):
    db_image = db.query(models.Image).filter(models.Image.id == image_id).first()
    db.delete(db_image)
    db.commit()

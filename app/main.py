from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from . import models, schemas, crud, dependencies, aws_utils

app = FastAPI()

models.Base.metadata.create_all(bind=dependencies.engine)

@app.post("/upload/", response_model=schemas.Image)
async def upload_image(file: UploadFile = File(...), db: Session = Depends(dependencies.get_db)):
    s3_url = await aws_utils.upload_image_to_s3(file)
    return crud.create_image(db=db, image=schemas.ImageCreate(name=file.filename, url=s3_url, type=file.content_type))

@app.get("/images/{image_id}", response_model=schemas.Image)
def read_image(image_id: int, db: Session = Depends(dependencies.get_db)):
    db_image = crud.get_image(db, image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

@app.delete("/images/{image_id}")
def delete_image(image_id: int, db: Session = Depends(dependencies.get_db)):
    db_image = crud.get_image(db, image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    aws_utils.delete_image_from_s3(db_image.url)
    crud.delete_image(db=db, image_id=image_id)
    return {"detail": "Image deleted successfully"}

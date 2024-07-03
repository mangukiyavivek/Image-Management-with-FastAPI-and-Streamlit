from pydantic import BaseModel

class ImageBase(BaseModel):
    name: str
    url: str
    type: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int

    class Config:
        from_attributes = True  # Updated for Pydantic V2

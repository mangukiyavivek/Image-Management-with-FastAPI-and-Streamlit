from sqlalchemy import Column, Integer, String
from .dependencies import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)

from pydantic import BaseModel

class ColumnCreate(BaseModel):
    name: str

class ColumnOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
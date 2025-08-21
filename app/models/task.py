from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.database import Base

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    column_id = Column(Integer, ForeignKey('columns.id'))
    position = Column(Integer),
    user_id = Column(Integer, ForeignKey('users.id'))


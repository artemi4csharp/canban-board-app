from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.schemas.column import ColumnCreate, ColumnOut
from app.models.user import User
from app.models.column import Column, BoardColumn
from app.dependencies import get_db
from app.auth.auth import get_current_user

router = APIRouter(prefix='/column', tags=['column'])

@router.post('/create', response_model=ColumnOut)
def create_column(column: ColumnCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_column = Column(
        name=column.name,
        user_id=user.id,
        user=user
    )
    db.add(new_column)
    db.commit()
    db.refresh(new_column)
    return new_column

@router.get('/', response_model=list[ColumnOut])
def get_columns(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(BoardColumn).filter_by(user_id=user.id).all()

@router.put('/update/{column_id}', response_model=ColumnOut)
def update_column(column_id : int, column: ColumnCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_column = db.query(BoardColumn).filter_by(id=column_id, user_id=user.id).first()
    if not db_column:
        raise HTTPException(status_code=404, detail='Column not found')
    db_column.name = column.name
    db.commit()
    db.refresh(db_column)
    return db_column

@router.delete('/delete/{column_id}')
def delete_column(column_id : int, db: Session = Depends(get_db)):
    db_column = db.query(BoardColumn).filter_by(id=column_id).first()
    if not db_column:
        raise HTTPException(status_code=404, detail='Column not found')
    db.delete(db_column)
    db.commit()
    return {'message': 'Column deleted successfully!'}
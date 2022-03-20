from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags = ['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)    
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash the password - user.password
    hashed_password = utils.hash(user.password)

    #сохраняем захешированный пароль в pydantic модели
    user.password = hashed_password

    #**user.dict() - преобразование в словарь pydatntic и его распаковка **
    new_user = models.User(**user.dict())
    #добавление юзера в базу и сохранение изменений
    db.add(new_user)
    db.commit()
    #аналог SQL-команды RETURNING
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'User with id: {id} does not exist')
    
    return user
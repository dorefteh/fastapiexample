from os import access
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags = ["Authentication"])

'''создаем операцию пути для проверки при входе в приложение. В переменной user_credentials
мы станавливаем зависимость на форму запроса пароле. Данные о почте в форме будут
сохранятся в поле username. Сама почта будет представлять собой словарь
{
    "username" : "something"
    "password" : "something"
}
'''
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f'Invalid Credentialds')
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f'Invalid Credentialds')
    #создаем токен. Data - содержит данные, предоставление которых мы сочтем нужным
    access_token = oauth2.create_acces_token(data = {"user_id" : user.id})
   
    #передаем токен
    return {"access_token": access_token, "token_type": "bearer"}
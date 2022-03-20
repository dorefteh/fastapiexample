from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings

#создаем переменную, которая будет предъявлять пароль
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

'''нам нужно предоставить:
секретный ключ
алгоритм
срок годности токена
'''

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_acces_token(data: dict):
    #в to_encode будут содержаться данные, которые будут закодированны в токен
    to_encode = data.copy()
    #переменная для установки срока годности
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

'''создаем функцию для проверки токена. Она будет декодировать jwt, извлекать id,
если id нет - появится ошибка, затем в переменной token_data она утверждает
данные (в нашем случае только id) и возвращает значение этой переменной'''
def verify_access_token(token: str, credentials_exeption):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)


        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exeption

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exeption

    return token_data

'''Создаем функцию, которая мы сможем ставить её в качестве зависимости к любой
из операций пути. Далее она будет автоматически забирать токен запроса, извлекать
id для нас, сообщать, является ли токен верным, обращаясь к функции 
verify_access_token. Затем, если нам нужно, мы можем выбирать пользователя и 
добавлять его как параметр в наши операции пути'''

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user

'''Объяснение: Для того, чтобы ограничить доступ для неавторизованных пользователей,
мы создадим еще одну зависимость, которая будет принимать резултат проверки функции
get_current_user'''


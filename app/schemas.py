from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

#класс для создания пользователей
class UserCreate(BaseModel):
    email: EmailStr
    password: str

#класс для получения пользователем данных при создании аккаунта
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


#класс для аутентификации
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#здесь создаем класс, который расширяет модель из библиотеки pydantic и установим его свойства
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

#схема при создании поста
class PostCreate(PostBase):
    pass

#Класс для отправки ответов на запросы
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    #Этот класс нужен для конвертации модели ORM(sqlalchemy в нашем случае) в модель pydantic 
    class Config:
        orm_mode = True

'''класс для вывода объединенных таблиц vote и posts сгруппированных по posts.id
 с подчетом голосов для каждого поста. В самом классе первый Post относится к
 названию словаря из вывода JOIN, который был прописан с заглавной, поэтому
 в схеме Post также прописан с заглавной.
 Второй Post ссылается на pydantic схему Post, что выше'''
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


#класс для jwt токенов
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


#класс для голосов. dir - direction
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)




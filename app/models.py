from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .database import Base

#Расширяем модель из файла database.py - создаем таблицу
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    #создадим отношение, ссылаясь на класс User
    owner = relationship("User")
'''SQLalchemy не предназначена
для изменения содержания таблиц и свойтств её атрибутов. Для того, чтобы изменения
подействовали, нужно пересоздать таблицу. 
SQLalchemy будет создавать таблицу с определенным именем только если таблицы с таким
именем нет в БД'''

#создаем таблицу для хранения данных о пользователе. Base - класс для каждой модели sqlaslchemy
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number=Column(String)

#создаем модель для голосов
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True )
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True )



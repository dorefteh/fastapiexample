from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

'''Формат, который мы должны передать sqlalchemy: 'postgresql://<username>:<password>@<ip-adress/hostname>/<database_name>'''
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

#Создаемм движок - он будет ответственнен за установку подключения sqlalchemy к postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)
'''Если мы будем использовать SQLite базу данных, то следует указывать вторым
параметром следующее - connect_args={"check_same_thread": False}'''

#Создаем сессию, через которую мы будем взаимодействовать с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Базовый класс, который будет вмещать все модели, таблицы и т.д 
Base = declarative_base()


'''зависимость. Эта запись станавливает связь (сессию) с базой данных. каждый раз,
когда к нам будет поступать запрос будет устанавливаться сессия, мы можем посылать
через сессию SQL утверждения и после выполнения запроса сессия будет заканчиваться'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


    '''Использование SQL напрямую
    Здесь мы применяем библиотеку psycorg и создаем код для подключения к базе данных.
Она является адаптером PostgresQL для python. cursorfactory = RealDictCursor нужна
для получения данный о названиях столбцов атрибутов + о информации под ними.
Переменная cursor содержить метод cursor объекта conn. Пользуясь этой переменной, 
мы будем выполнять SQL-команды. Цикл while будет повторяться, пока не появится 
подключение с задержкой в 5 секунд.'''

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#         password='U6574./gye68', cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(5)

#Графа published здесь является опциональной, так как
#мы указали для неё дефолтное значение - True. Но если пользователь заполнит это поле (например false) - сервер это учтет

#Граффа rating будет опциональной но не будет иметь дефолтного значения

#Здесь мы создаем множество из постов, которые будут представлять собой словари данных
# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite food", "content":"i like pizza", "id": 2}]
#Эти данные сохраняются в памяти и будут теряться с каждым перезапуском приложения


#здесь созхдаем функциюдля поиска ай ди постов
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
#выше мы проитерировали my_posts по постам - p и по их индексам - i
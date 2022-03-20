from email.policy import HTTP
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


#Эта запись создает все наши модели
'''Команда ниже говорит sqlalchemy запускать create-утверждения, которые создают 
все столбцы. Так как теперь у нас есть для этого alembic, эта команда больше не 
нужна'''
# models.Base.metadata.create_all(bind=engine)

#фастапи конвертирует то, что под функцией в json
#request Get method url: "/"
app = FastAPI()
#переменная с допустимыми доменами
# origins = ["https://www.google.ru", "https://www.youtube.com/"]
origins = ["*"]
'''Метод для изменения политики CORS, чтобы нам могли отправлять запросы с других
домен на домен с нашим сервером. Middleware - это такая функция, которая запускается
перед каждым запросом. В allow_origins - мы помещаем домены, которым даём разрешение
делать запросы нашему серверу. Запись allow_origins=["*"] - говорит, что мы
разрешаем делать запросы всем доменам(wildcard). 
В allow_methods - мы устанавливаем допустимые 
HTTP-методы запросов
'''
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#здесь включаем маршрутизаторы user и post в наш API
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

'''Для того, чтобы импортировать файлы из папки на один уровень выше, нужно прописать две точки
перед названием файла, из которого будет происходить импорт.'''
#с помощью инстанса app мы применяем к функции фастапи для трансформации json(указывая None)
@app.get("/")
def root():
    return {"message": "welcome to my api!!"}

'''Мы изменили функцию def_posts так, что она возвращает на сервер данные,
которые запрашивались по url.
Добавили:
posts = cursor.execute(три кавычки SELECT * FROM posts три кавычки)
    posts = cursor.fecthall
    return {"data": my_posts}
    '''


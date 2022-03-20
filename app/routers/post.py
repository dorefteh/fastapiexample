from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from app.oauth2 import get_current_user
from .. import schemas, models, oauth2
from ..database import get_db

'''Создаем объект маршрутизатора. Каждый такой объект будет включен в инстантс
FastAPI (в нашем случае он назуывается app).
Префикс будет добавлятся к началу пути каждой функции, чтобы не приходилось
прописывать его нескольо раз.
Tags(ярлыки) нужны для групировки функций в UI нашего приложения (http://127.0.0.1:8000/docs)
'''
router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)


# Создаем операцию-пути для тестирования ORM сессий
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     #создает запрос, который будет эквивалентен select * from posts;
#     posts = db.query(models.Post).all()
#     return {"data": posts}


'''Добавим в функцию get_posts параметры запроса. Параметр запроса здесь - limit'''
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(
    oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] =""):
    #закоментированные строки - запрос с использ. SQL
    # posts = cursor.execute('''SELECT * FROM posts ''')
    # posts = cursor.fetchall()
    #ниже запрос без использования join для получения инф. об голосах
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(
    #     limit).offset(skip).all()

    '''создаем запрос базе данных через ORM с использование JOIN, COUNT, GROUP BY. 
    Стоит заметить, что по умолчанию sqlalchemy использует LEFT INNER JOIN.
    А когда мы использовали чистый SQL в pgadmin, а именно команды LEFT/RIGHT JOIN,
    то, по сути, мы пользовались LEFT OUTER JOIN. Поэтому в join мы указали
    аргумент isouter'''
    posts = db.query(models.Post, func.count(
        models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(
        skip).all()
    
    return posts

'''важно знать одну вещь о фастапи: всякий раз, когда мы делаем 
запрос на сервер апи, апи просматривает лист наших всех
наших путевых операций(например:@app.get("/")), и когда он находит 
первое совпадение - код перестает выполняться.
Так если мы пропишем две операции, которые будут происходить при 
переходе по одному пути(url), то будет выполнена только первая.
Вырезанный код из def create_post:
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)

    %s - представляет собой некую переменную (placeholder).
    Такая запись кода (с использованием %s и выведением параметров для заполнение
    во второе окно) cursor.execute необходима, чтобы предотвратить потенциальноу
    управление базой SQL из вне путем записы SQL запросов в постах. 
    Если записать код как f три кавычки insert ... {post.title}... - то такая
    управление со стороны будет возможно.
    Порядок записи значений должен соответствовать порядку атрибутов
'''

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #**post.dict() - распаковка словаря pydantic модели
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    #добавление поста в базу и сохранение изменений
    db.add(new_post)
    db.commit()
    #аналог SQL-команды RETURNING
    db.refresh(new_post)
    return new_post


''' 
примененние SQL к функции create_post
# cursor.execute(три кавычки INSERT INTO posts (title, content, published) 
# VALUES (%s, %s, %s) RETURNING * три кавычки,
# (post.title, post.content, post.published))
#запись для получения всех данных
# new_post = cursor.fetchall()
#запись для сохранения изменений в базе
# conn.commit()
#**post.dict() - распаковка словаря нашей схемы.
# '''

#title str, content str
'''Благодаря тому, ипользованию экземпляра new_post, fastapi будет автоматически проверять данные на соответсвие нашим критериям. В данном случае содержание content и title должно быть строкой'''
#def create_post(payload: dict = Body(...))
#return {"new_post": f"title {payload['title']} content: {payload['content']}"}
#print(new_post.published)
'''Мы можем в теле функции указать после экземпляра через точку название типа данных, который нас интересует в данный момент, и сервер будет показывать только их. Если данные, отправленыне пользователем не будут отправлены или будут отправлены в неправильном формате (данные не будут соответствовать классу Post) произойдет ошибка, которая не позволит пользователю отправить запрос.
Стоит отметить, что pydantic будет пытаться конвентировать данные в строку. Так, если на сервер будут посланы данные в формате int, то pydantic конвентирует их str.
Вывод: с помощью pydantic производится проверка данных фронтэнла на соответствие
модели BaseModel

Каждая модель в pydantic имеет метод .dict, с помощью которого
мы можем конвертировать модели в словарь
'''

#Здесь создаем функцию для получения одного индивидуального поста

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #Применение SQL
    #конвертируем id в строку, чтобы SQL команда сработала
    #нужно исправить на '(str(id),)' если будет возникать ошибка
    # cursor.execute('''SELECT * FROM posts WHERE id = %s''', (str(id)))
    # post = cursor.fetchone()
    #ниже запрос без join
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    #запрос с JOIN, COUNT, GROUP BY
    post = db.query(models.Post, func.count(
        models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found")
    return post


'''Если пользователь запрашивает пост который не существует, то будет
выводится соответствующий ответ. Формируется ответ с помощью библиотек:
Response - которая позволяет конфигурировать ответы; status - позволяющая
не запоминать коды статуса, а выбирать их из списка с кратким описанием;
HTTPExeption - класс с параметрами для кода статуса и сообщения.

Можно задавать статус коды по умолчанию указывая их в декораторе, после
пути.



id в /posts/{id} является параметром пути. Важно помнить, что 
параметры пути всегда будут иметь текстовый формать. Так что в
переменной post, использующей функцию find_post( которая принимает
в качестве аргумента id) мы изменили тип id на целочисленный, чтобы
функция работала как надо.
Далее мы изменили код так, что id будут
конвертироваться в самой функции, и нам не нужно делать это вручную:
будет осуществляться проверка запроса пользователя по типу данных
параментра пути - id. В нашем случае, пользователь, который отправил
в качестве id строку будет получать ошибку.
'''

#создаем функцию по удалению постов
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #применение SQL
    # cursor.execute(
    #     '''DELETE FROM posts WHERE id = %s returning *''', (str(id)))
    # deleted_post = cursor.fetchone()

    # conn.commit()


    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=
        "Not autherized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    
    return Response(status_code = status.HTTP_204_NO_CONTENT)

#функция для изменения поста. Будем использовать класс Post (созданный ранее), 
#поскольку он содержит схему, которой фронт-энд будет пользоваться при 
#во время PUT-запросов
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    #применение SQL
    # cursor.execute('''UPDATE posts SET title = %s, 
    # content = %s, published = %s WHERE id = %s 
    # RETURNING *''', (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    #сохраняем запрос
    post_query = db.query(models.Post).filter(models.Post.id == id)

    #
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=
        "Not autherized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
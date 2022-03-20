from passlib.context import CryptContext

#настраиваем с помощью passlib алгоритм хеширования
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#определим функцию для хеширования
def hash(password: str):
    return pwd_context.hash(password)


#создаем функцию, котороая будет хэшировать введенный пароль и сравнивать его с паролев в БД
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

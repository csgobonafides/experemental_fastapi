import jwt
from fastapi import FastAPI, Request
from datetime import timedelta

SECRET_KEY = 'secretkey'
ALGORITM = 'HS256'

USER_DATA = [
    {"username": "bona", "password": "admin"}
]

app = FastAPI()

def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITM)

def get_user_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITM)
        return payload.get('name'), payload.get('rolls')
    except jwt.ExpiredSignatureError:
        return 'Error ExpiredSignatureError'
    except jwt.InvalidTokenError:
        return 'Error InvalidTokenError'

def get_user(username: str):
    for user in USER_DATA:
        if user.get('username') == username:
            return user
    return None

def name_chek(name):
    for user in USER_DATA:
        if user.get('username') == name:
            return False
    return True

def authentifick(name, psw):
    for user in USER_DATA:
        if user.get('username') == name and user.get('password') == psw:
            token = create_jwt_token({'name': f'{name}', 'rolls': 'user'})
            return {'Вы успешно зарегистрированы, вот ваш токен': token}
        elif user.get('username') == name and user.get('password') != psw:
            return {'Вы указали неверный': 'пороль.'}
    return {'Пользователь с такими данными': 'не найден.'}

def registed(name, psw):
    if not name_chek(name):
        return {'Пользователь с таким логином': 'уже зарегистрирован.'}
    else:
        USER_DATA.append({'username': f'{name}', 'password': f'{psw}'})
        return {'Вы успешно зарегистрированы': 'ok'}



@app.post('/reg/{login}/{psw}')
async def reg(login, psw):
    return registed(login, psw)

@app.post('/auth/{login}/{psw}')
async def auth(login, psw):
    return authentifick(login, psw)

@app.post('/about_me')
async def about_me(request: Request):
    print(request.headers.get('authorization'))
    if request.headers.get('authorization'):
        result = get_user_from_token(request.headers.get('authorization')[7:])
        print(result)
        if result == 'Error ExpiredSignatureError':
            return 'Error ExpiredSignatureError'
        if result == 'Error InvalidTokenError':
            return 'Error InvalidTokenError'
        else:
            return f'Рады вас приветствовать {result[0]}'
    else:
        return 'Error'



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1')
from fastapi import FastAPI, Request, Response, Cookie
from datetime import timedelta, datetime
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

app = FastAPI()

SECRET_KEY = 'secretkey'
ALGORITM = 'HS256'
USER_DATA = [{'login': 'bona', 'psw': '123'}]

def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITM)

def get_user_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITM)
        return {'login': payload.get('login'), 'password': payload.get('psw')}
    except jwt.ExpiredSignatureError:
        raise ExpiredSignatureError
    except jwt.InvalidTokenError:
        raise InvalidTokenError

def chek_user(lg, psw):
    for user in USER_DATA:
        if user.get('login') == lg and user.get('psw') == psw:
            return True
    return False

@app.get('/one')
async def one(login, psw, response: Response):
    if chek_user(login, psw):
        token = create_jwt_token({'login': login, 'psw': psw})
        response.set_cookie(key='my_cookie', max_age=60, value=token)
        return {'message': 'Куки установлены.'}
    return {'message': 'Данные не верны.'}

@app.get('/two')
async def two(request: Request):
    if request.headers.get('cookie'):
        print(request.headers.get('cookie'))
        print(request.headers.get('cookie')[10:])
        return get_user_from_token(request.headers.get('cookie')[10:])
    return {'message': 'Not authenticate'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1')
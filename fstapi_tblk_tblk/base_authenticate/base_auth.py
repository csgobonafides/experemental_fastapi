from fastapi import FastAPI, Depends, status, HTTPException, Request
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import jwt

app = FastAPI()
security = HTTPBasic()

class User(BaseModel):
    username: str
    password: str

SECRET_KEY = 'secretkey'
ALGORITM = 'HS256'
USER_DATA = [User(**{"username": "user1", "password": "pass1"}), User(**{"username": "user2", "password": "pass2"})]


'''Если пользователь зареган, проверяем пороль.'''
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user


'''Проверка логина. Есть ли такой пользователь.'''
def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None


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



'''Защита ручки, используя функцию проверки пороля как зависимость.'''
@app.get("/protected_resource/")
def protected_resource(user: User = Depends(authenticate_user)):
    token = create_jwt_token({'name': f'{user.username}', 'rolls': 'user'})
    return {"message": "You have access to the protected resource!", "user_info": user, 'token': {token}}

@app.get('/about_me')
async def about_me(request: Request):
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
        return 'Отсутствует Токен.'

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1')

'''Для выполнения ручки, необходимо сначала ввести лгин и пороль 1 раз.'''
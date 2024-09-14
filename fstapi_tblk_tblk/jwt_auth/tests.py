from fastapi import FastAPI, Request, Response, Cookie
from datetime import timedelta, datetime

app = FastAPI()


'''Создание и передача cookie с датой последнего визита и временем жизни 60сек.'''
@app.get('/root')
async def root(response: Response):
    now = datetime.now()
    response.set_cookie(key='last_visit', max_age=60, value=now)
    return {'message': 'куки установленны.'}


'''Проверка cookie.'''
@app.get('/visit')
async def visit(request: Request, last_visit: str | None = Cookie(default=None)):
    print(request.headers.get('cookie'))
    if last_visit == None:
        return {'message': 'Это ваш первый визит.'}
    else:
        return {'message': f'Ваш последний визит был {last_visit}'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1')
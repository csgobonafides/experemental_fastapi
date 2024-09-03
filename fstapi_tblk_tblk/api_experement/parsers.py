import asyncio
from bs4 import BeautifulSoup
from urllib.parse import quote
import aiohttp
import re

async def data_film(name_film: str):
    url = 'https://www.google.com/search?q=' + quote('дата выхода фильма' + name_film)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'}) as response:
            soup = await response.text()
            bs = BeautifulSoup(soup, 'html.parser')
            result = bs.find('div', {'class': 'Z0LcW t2b5Cf'})
            if result:
                print(f'Дата выхода фильма {name_film} - {result.text}.')
                return {f'Дата выхода фильма {name_film}': result.text}
            else:
                print('Не удалось найти информацию об этом фильме.')
                return {'Error': 'Не удалось найти информацию об этом фильме.'}

async def comand_install_bibl(name_bibl: str):
    url = 'https://pypi.org/project/' + name_bibl
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            soup = await response.text()
            bs = BeautifulSoup(soup, 'html.parser')
            result = bs.find('span', {'id': 'pip-command'})
            if result:
                print(f'Для установки билбиотеки {name_bibl}, введите {result.text} в терминате.')
                return {f'Для установки билбиотеки {name_bibl}, введите в терменале команду': result.text}
            else:
                print(f'Не удалось найти {name_bibl} библиотеку, проверьте правильность его написания.')
                return {f'Error': f'Не удалось найти {name_bibl} библиотеку, проверьте правильность его написания.'}



async def registr(log, psw):
    with open('db.txt', 'r+') as file:
        lg = re.search(f'{log}:{psw}', file.read())
        if lg:
            return f'Пользователь с логином {log} уже зарегистрирован.'
        else:
            file.write(f'{log}:{psw}\n')
            return f'Пользователь {log} успешно зарегистрирован.'

async def autoris(log, psw):
    with open('db.txt', 'r') as rd:
        lg = re.search(f'{log}:{psw}', rd.read())
        if lg:
            return f'Пользователь {log} успешно авторизировался.'
        else:
            return 'Вы указали неверный логин или пороль.'

asyncio.run(registr('bona', '123'))
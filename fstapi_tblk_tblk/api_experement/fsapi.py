import asyncio
from fastapi import FastAPI
from fstapi_tblk_tblk.api_experement.parsers import data_film, comand_install_bibl, registr, autoris

app = FastAPI()

@app.post('/film/{name_film}')
async def data_films(name_film: str):
    return await data_film(name_film)

@app.post('/bibl/{name_bibl}')
async def data_bibl(name_bibl: str):
    return await comand_install_bibl(name_bibl)

@app.post('/register/{login}/{password}')
async def register(login, password):
    return await registr(login, password)

@app.post('/autorisation/{login}/{password}')
async def autorisation(login, password):
    return await autoris(login, password)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1')
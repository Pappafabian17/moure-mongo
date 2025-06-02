from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles
app = FastAPI()
#routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/",tags=["Main"])
async def root():
  return "!Hola Fastapi!"

@app.get("/url",tags=["Main"])
async def url():
  return {"url_curso":"https://mouredev.com"}

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


#Entidfad user 

class User(BaseModel):
  id:int
  name: str
  surname: str
  url: str
  age: int
  

users_list = [
  User(id= 1, name="fab", surname="pappa", url="asdas@lokita.com", age=25),
  User(id= 2,name="joe", surname="pappa", url="joe@sapent.com", age=25),
  User(id= 3,name="her", surname="pappa", url="her@sape.com", age=23)
]


@app.get("/usersjson")
async def usersjson():
  return [{"name":"Fabian", "surname":"pappa","url":"Fabianpappa.com", "age":25},
          {"name":"joel", "surname":"pappa","url":"joelcito.com", "age":25},
          {"name":"hernan", "surname":"pappa","url":"hernancito.com", "age":23}]

@app.get("/users")
async def users():
  return users_list

@app.get("/user/{id}")
async def user(id : int ):
  return search_user(id)
  
  

@app.get("/user/")
async def user(id : int ):
  return search_user(id)
  

@app.post("/user/")
async def user(user : User):
  if type(search_user(user.id)) == User:
    return {"error":"El usuario ya existe"}
  else :
    users_list.append(user)


def search_user(id : int):
  users = filter(lambda user : user.id == id, users_list)
  try:
    return list(users)[0]
  except:
    return {"error" : "No se ha encontrado el usuario"}
  



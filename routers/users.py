from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["usuario"])


#Entidfad user 

class User(BaseModel):
  id: int
  name: str
  surname: str
  url: str
  age: int

# Modelo para registro de usuario
class UserRegister(BaseModel):
  name: str
  surname: str
  url: str
  age: int



# Lista de usuarios registrados
users_list = [
  User(id=1, name="fab", surname="pappa", url="asdas@lokita.com", age=24),
  User(id=2, name="joe", surname="pappa", url="joe@sapent.com", age=24),
  User(id=3, name="her", surname="pappa", url="her@sape.com", age=23)
]

  


@router.get("/usersjson")
async def usersjson():
  return [{"name":"Fabian", "surname":"pappa","url":"Fabianpappa.com", "age":25},
          {"name":"joel", "surname":"pappa","url":"joelcito.com", "age":25},
          {"name":"hernan", "surname":"pappa","url":"hernancito.com", "age":23}]

@router.get("/users")
async def users():
  return users_list

@router.get("/user/{id}")
async def user(id : int ):
  return search_user(id)
  
  

@router.get("/user/")
async def user(id : int ):
  return search_user(id)
  
#  ---------------POST-------------------
@router.post("/user/",response_model=User ,status_code=201)
async def user(user : User):
  if type(search_user(user.id)) == User:
    raise HTTPException(status_code=404, detail="El usuario ya existe")
  else :
    users_list.append(user)
    return user
#  ---------------PUT--------------------
@router.put("/user/")
async def update_user(user:User):
    for index, saved_user in enumerate(users_list):
      print(f"userID=={user.id}")
      print(f"saved_userID=={saved_user.id}")
      if saved_user.id == user.id:
        
        users_list[index] = user 
        return user
      
      

@router.delete("/user/{id}")
async def delete_user(id:int):
  usuario = search_user(id)
  users_list.remove(usuario)
  return {"message":"usuario eliminado correctamente "}


print(users_list)
def search_user(id : int):
  users = filter(lambda user : user.id == id, users_list)
  try:
    return list(users)[0]
  except:
    return {"error" : "No se ha encontrado el usuario"}
  



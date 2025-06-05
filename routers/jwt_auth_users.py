from fastapi import Depends,HTTPException, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 
SECRET = "02b1b9s2f65hgf0198e3d612wq36f82j"
router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
  username:str
  full_name: str
  email:str
  disabled:bool

class UserDB(User):
  password:str

users_db = {"fabian":{
    "username":"fabian",
    "full_name": "Fabian pappa",
    "email":"fabian@gmail.com",
    "disabled": False,
    "password": "$2a$12$lN1k5FtIk3U.3l7F9.xKSenCGDHrvF.m6Kf8SHjdeYC9CjHNAcCc."
  },
  "fabian2":{
    "username":"fabian2",
    "full_name": "Fabian pappa2",
    "email":"fabian2@gmail.com",
    "disabled": True,
    "password": "$2a$12$IEn9/wjLhW0AO8B/ejTXCOHpca9Tfmh6ERBfOgqwhWwt7N0S8f6XG"
  }}

def search_user_db(username: str):
  if username in users_db:
    return UserDB(**users_db[username])
  
def search_user(username: str):
  if username in users_db:
    return User(**users_db[username])

@router.post("/login")
async def login(form : OAuth2PasswordRequestForm  = Depends()):
  user_db = users_db.get(form.username)
  if not user_db:
    raise HTTPException(status_code = 400, detail= "El usuario no es correcto")
  user = search_user_db(form.username)

  
  if not crypt.verify(form.password, user.password):
    raise HTTPException(status_code = 400, detail= "La contrasena no es correcto")
  
  access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION)
  expire = datetime.now(timezone.utc) + access_token_expiration

  access_token = {
    "sub": user.username,
    "exp": expire}

  return {"access_token": jwt.encode(access_token , SECRET ,algorithm=ALGORITHM), "token_type":"bearer"}

async def auth_user(token: str = Depends(oauth2)):
  exception = HTTPException(status_code=400, detail="Credenciales de autenticacion invalidas ", headers={"www-authenticate " : "Bearer"})
  try:
    username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
    if username is None:
      raise exception
    user = search_user(username)
    if user is None:
      raise exception
    return user


  except JWTError:
    raise exception

async def current_user(user: User = Depends(auth_user)):
  
  
  if user.disabled:
    raise HTTPException( status_code= 400, detail="Usuario inactivo")
  return user
  
@router.get("/users/me")
async def me(user: User = Depends(current_user)):

  return user 
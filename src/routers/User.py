from fastapi import APIRouter, HTTPException, status, Header, Query
from fastapi.responses import JSONResponse
from ..DataControler import dataBase
from src.models.UserModel import UserLoged,UserRegisted
import src.models.secure as secure
import os




db = dataBase.DataBase()
router = APIRouter()


@router.get("/users")
async def getUsers():
    return db.obtener_usuarios()


@router.post("/login",status_code=status.HTTP_202_ACCEPTED)
async def login(user: UserLoged):
    
    if not(db.usuario_exist(user.email)):
        raise HTTPException(status_code=404,detail="Usuario no existe")
        
    passwEncript = db.getUserPass(user.email)
    salt = db.getUserSalt(user.email)
    if not(secure.validatePassword(user.passw,passwEncript,salt)):
        raise HTTPException(status_code=406,detail="La contraseña es incorrecta")
    
    premium = db.usuario_es_de_pago(user.email)
    return {"token": secure.generateToken({'email': user.email.strip(), 'premium' : premium})}
    
        
    


@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register(user: UserRegisted):
    
    if (db.usuario_exist(user.email) == False):
        db.insertar_usuario(user)
        ruta = "./Data/"+user.email
        os.mkdir(ruta)
        return {"message": "User registered successfully."}
    else:
        raise HTTPException(status_code=406, detail="User is registed")



@router.get("/myInfo")
async def getMyInfo(authorization: str = Header(None)):

    tokenInfo = secure.decriptToken(authorization)

    email = tokenInfo.get("email")
    premium = tokenInfo.get("premium")

    userInfo = {
        "email": email,
        "name": db.getUserName(email),
        "premium": premium,
        "telefono": db.getUserPhone(email)
    }

    return userInfo

@router.get("/user/changePass")
async def changePass(oldPassword: str = Query(None), newPassword: str = Query(None),authorization: str = Header(None)):

    tokenInfo = secure.decriptToken(authorization)

    email = tokenInfo.get("email")
    userEncriptedPass = db.getUserPass(email)
    userSalt = db.getUserSalt(email)


    if not(secure.validatePassword(oldPassword,userEncriptedPass,userSalt)):  
        raise HTTPException(status_code=409,detail="La contraseña actual no es correcta")

    db.changeUserPass(newPassword,email)
    print("Ok tu contraseña es valida")

    return JSONResponse(status_code=200,content={"password":"A sido actualizada correctamente"}) 

    

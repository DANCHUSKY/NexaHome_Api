from fastapi import HTTPException
from hashlib import sha512
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from dotenv import load_dotenv
import os

env_path = './src/DataControler/.env'

load_dotenv(dotenv_path=env_path)

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutos
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 # 1 dia
SECRET_KEY = os.getenv('SECRET_KEY')

def encrypt(password):
    # Generar una sal aleatoria
    salt = os.urandom(16)  # 16 bytes (128 bits) de sal aleatoria
    
    # Concatenar la sal con la contraseña
    salted_password = salt + password.encode('utf-8')
    
    # Calcular el hash usando SHA-512
    hashed_password = sha512(salted_password).hexdigest()

    return [hashed_password, salt]


def validatePassword(password,hashedpassword,salt):
    #Transforma el salt a bytes
    decoded_salt = bytes.fromhex(salt[2:])
    #Crea la contraseña hashed con el salt y la compara
    hashed_input_password = sha512(decoded_salt + password.encode('utf-8')).hexdigest()

    if(hashed_input_password == hashedpassword):
        return True
    else:
        return False


def generateToken(info: dict):
    if SECRET_KEY is None:
        raise ValueError("La clave secreta no puede ser None.")
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    info.update({"exp": expire})
    token = jwt.encode(info, SECRET_KEY, algorithm='HS512')
    return token

def decriptToken(token: str):
    try:
        # Intenta decodificar el token.
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS512'])
        return decoded_token
    except JWTError:
        # Si el token no es válido (por ejemplo, si fue modificado), se lanzará una excepción.
        raise HTTPException(status_code=401,detail="invalid token")
    

def validateToken(token: str):
    try:
        # Intenta decodificar el token.
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS512'])
        return True
    except JWTError:
        # Si el token no es válido (por ejemplo, si fue modificado), se lanzará una excepción.
        return False
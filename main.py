from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.routers import User, Propiedad
import src.models.secure as secure
from src.DataControler.dataBase import DataBase
import os

db = DataBase()
app = FastAPI()

# Define allowed origins
origins = [
    "*"
]

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],           # Allow all methods
    allow_headers=["*"],           # Allow all headers
)

# Routers
app.include_router(User.router)
app.include_router(Propiedad.router)

#AJUSTAR PARA HTTPS
@app.middleware("http")
async def auth_middleware(request: Request, call_next):

    #TEMPORAL QUITAR CUANDO SSL
    if request.method == "OPTIONS":
      response = await call_next(request)
      return response

    # Verificar si la ruta requiere autenticación
    if request.url.path not in ["/login", "/register","/"]:
        # Recuperar el token de los headers
        token = request.headers.get("Authorization")

        # Verificar si el token está presente
        if not token:
            # Si no hay token, devolver error 401
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "No autorizado - Token no encontrado en los headers"})

        # Validar el token
        is_valid = secure.validateToken(token)
        if not is_valid:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Token inválido o expirado"}) 
    # Si la validación del token es correcta o la ruta no requiere autenticación, proceder con la solicitud
    response = await call_next(request)
    return response

@app.get("/")
async def index():
    return {"Message": "Hello"}

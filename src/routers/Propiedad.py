from fastapi import APIRouter, HTTPException,status, File, UploadFile, Header, Query
from ..DataControler import dataBase
from pydantic import ValidationError
from starlette.background import BackgroundTask
from starlette.responses import FileResponse
from src.models.PropiedadModel import Propiedad
from typing import List

import src.models.secure as secure
import json, os, zipfile, traceback




db = dataBase.DataBase()
router = APIRouter()




#Metodos de busqueda

@router.get("/property/myProperty")
async def getProperty(authorization: str = Header(None)):
    tokenInfo = secure.decriptToken(authorization)
    email = tokenInfo.get("email")
    return db.getMyPropertys(email)

@router.get("/property/allProperty")
async def getProperty(position: int = Query(None),authorization: str = Header(None)):
    return db.getPropertyInRange(position)

@router.get("/property/getByCity")
async def getPropByCity(city: str = Query(None),authorization: str = Header(None)):
    return db.getPropertyByCity(city)

#Fin metodos busqueda

@router.post("/property", status_code=status.HTTP_202_ACCEPTED)
async def insert_property(prop: Propiedad, authorization: str =  Header(None)):
    try:
        propMax = 1

        infoToken = secure.decriptToken(authorization)
        premium = infoToken.get("premium")
        email = infoToken.get("email")

        if(premium):
            propMax = 5

        if(db.getPropertysCount(email) >= propMax):
            raise HTTPException(status_code=400, detail=f"Cantidad maxima de propiedades alcanzada")

        id = db.insert_property(email, prop)
        ruta = "./Data/"+email+"/"+str(id)
        
        if not os.path.exists(ruta):
            os.mkdir(ruta)

        return {"property": "Property added successfully","Id":id}

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"JSON mal formado: {str(e)}")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Error en la validación de datos: {str(e)}")

@router.post("/property/uploadimage")
async def insertImages(idProperty: int = Query(None), files: List[UploadFile] = File(...), authorization: str =  Header(None)):
    try:
        print(idProperty)
        print(db.PropertyExist(idProperty))
        if not db.PropertyExist(idProperty):
            raise HTTPException(status_code=404, detail="Item not found")
            
        
        email = secure.decriptToken(authorization).get("email")
        

        count = 1

        for file in files:
            # Obtener el nombre original del archivo y asegurar que no tenga espacios u otros caracteres problemáticos
            original_filename = file.filename
            name, extension = os.path.splitext(original_filename)
            safe_name = f"image-{count}{extension}"

            rute = "./Data/"+email+"/"+str(idProperty)+"/"+safe_name

            # Leer el contenido del archivo
            content = await file.read()
            

            # Escribir el contenido en el nuevo archivo en el directorio de destino
            with open(rute, 'wb') as archivo_destino:
                archivo_destino.write(content)


            count += 1

        return {"message": "Files successfully uploaded", "files": [file.filename for file in files]}

    except HTTPException as e:
        error_message = f"{str(e.__class__)}: {str(e)}"
        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
        full_error_message = f"HTTPException: {error_message}\nTraceback: {traceback_str}"
        print(full_error_message)
        raise e  # Re-raise HTTPException to keep the original status code

    except Exception as e:
        error_message = f"{str(e.__class__)}: {str(e)}"
        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
        full_error_message = f"General Exception: {error_message}\nTraceback: {traceback_str}"
        print(full_error_message)
        raise HTTPException(status_code=500, detail=full_error_message)

@router.get("/property/downloadimage")
async def getImages(idProperty: int = Query(None), authorization: str = Header(None)):
    try:
        if not db.PropertyExist(idProperty):
            raise HTTPException(status_code=404, detail="Item not found")

        email = secure.decriptToken(authorization).get("email")
        ruta = f"./Data/{email}/{idProperty}"
        
        if not os.path.exists(ruta):
            raise HTTPException(status_code=404, detail="Directory not found")

        listaImages = os.listdir(ruta)
        
        zip_filename = f"{email}_images.zip"
        zip_filepath = f"./tmp/{zip_filename}"
        
        os.makedirs("./tmp/", exist_ok=True)

        with zipfile.ZipFile(zip_filepath, "w") as zipf:
            for filename in listaImages:
                file_path = os.path.join(ruta, filename)
                if os.path.exists(file_path):
                    zipf.write(file_path, filename)
                else:
                    raise HTTPException(status_code=404, detail=f"File {filename} not found")

        return FileResponse(zip_filepath, filename=zip_filename, background=BackgroundTask(os.remove, zip_filepath))

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/property/iconImg")
async def getFirstImage(idProperty: int = Query(None), authorization: str = Header(None)):
    try:
        
        if not(db.PropertyExist(idProperty)):
            raise HTTPException(status_code=404, detail="La propiedad no existe o no se encuentra")
        
        email = db.getEmailProperty(idProperty)          
        ruta = f"./Data/{email}/{idProperty}"
        listaImages = os.listdir(ruta)

        if not(os.path.exists(ruta)):
            raise HTTPException(status_code=404, detail="El archivo no se a encontrado")
        
        image_path = os.path.join(ruta, listaImages[0])

        return FileResponse(path=image_path, filename=listaImages[0])
            


    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/property/contactInfo")
async def getContactInfo(idProperty: int = Query(None)):

    email = db.getEmailProperty(idProperty)
    name = db.getUserName(email)
    phone = db.getUserPhone(email)

    return {
        "name": name,
        "email": email,
        "phone": phone
    }


@router.delete("/property",status_code=status.HTTP_201_CREATED)
async def removeProperty():
    
    return {"Entraste a properti":"delete"}



from pydantic import BaseModel

class Propiedad(BaseModel):
    metrosCuadrados: int
    ciudad: str
    provincia: str
    calle: str
    numero: int
    precio: int
    estado: str
    parking: bool
    piscina: bool
    tipoPropiedad: str
    planta: int
    descripcion: str
    habitacion: int
    bano: int
    orientacion: str
    ascensor: bool
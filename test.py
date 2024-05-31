import requests,json


#Lista usuarios a registrarse
usuarios = [
    ['Juan', 'juan@example.com', 'contraseña1', '123456789'],
    ['Maria', 'maria@example.com', 'contraseña2', '987654321'],
    ['Pedro', 'pedro@example.com', 'contraseña3', '123123123'],
    ['Ana', 'ana@example.com', 'contraseña4', '321321321'],
    ['Luis', 'luis@example.com', 'contraseña5', '456456456'],
    ['Sofia', 'sofia@example.com', 'contraseña6', '654654654'],
    ['Carlos', 'carlos@example.com', 'contraseña7', '789789789'],
    ['Lucia', 'lucia@example.com', 'contraseña8', '987987987'],
    ['Fernando', 'fernando@example.com', 'contraseña9', '111222333'],
    ['Elena', 'elena@example.com', 'contraseña10', '444555666'],
    ['Gonzalo', 'gonzalo@example.com', 'contraseña11', '777888999'],
    ['Carmen', 'carmen@example.com', 'contraseña12', '222333444'],
    ['Jorge', 'jorge@example.com', 'contraseña13', '555666777'],
    ['Natalia', 'natalia@example.com', 'contraseña14', '888999000'],
    ['Miguel', 'miguel@example.com', 'contraseña15', '333444555'],
    ['Diana', 'diana@example.com', 'contraseña16', '666777888'],
    ['Oscar', 'oscar@example.com', 'contraseña17', '999000111'],
    ['Patricia', 'patricia@example.com', 'contraseña18', '444555666'],
    ['Roberto', 'roberto@example.com', 'contraseña19', '777888999']
]

#Lista propiedades a registrarse
propiedades = [
    ['juan@example.com', 120, 'Valencia', 'Valencia', 'Calle Sol', 10, 200000, 'nuevo', True, False, 'apartamento', 2, 'Luminoso y amplio', 'sur', True],
    ['maria@example.com', 90, 'Madrid', 'Madrid', 'Avenida Luna', 5, 250000, 'usado', False, True, 'casa', 0, 'Acogedor en buena zona', 'norte', False],
    ['pedro@example.com', 85, 'Sevilla', 'Sevilla', 'Plaza Jardín', 1, 180000, 'nuevo', True, True, 'apartamento', 3, 'Con vistas al parque', 'este', True],
    ['ana@example.com', 200, 'Zaragoza', 'Zaragoza', 'Calle Mayor', 20, 300000, 'usado', True, True, 'chalet', 0, 'Espacioso con jardín', 'oeste', False],
    ['luis@example.com', 150, 'Barcelona', 'Barcelona', 'Paseo Gracia', 15, 400000, 'nuevo', True, False, 'piso', 4, 'En pleno centro', 'sur', True],
    ['sofia@example.com', 100, 'Bilbao', 'Vizcaya', 'Calle Paz', 9, 220000, 'usado', False, False, 'duplex', 1, 'Recién reformado', 'norte', True],
    ['carlos@example.com', 130, 'Gijón', 'Asturias', 'Avenida Constitución', 8, 190000, 'nuevo', True, True, 'apartamento', 5, 'Ideal familias', 'este', True],
    ['lucia@example.com', 110, 'Alicante', 'Alicante', 'Calle Olvido', 2, 210000, 'usado', False, True, 'bungalow', 0, 'Cerca de la playa', 'oeste', False],
    ['fernando@example.com', 160, 'Córdoba', 'Córdoba', 'Ronda Tejares', 12, 230000, 'nuevo', True, False, 'chalet', 0, 'Con amplio patio', 'sur', True],
    ['elena@example.com', 140, 'Granada', 'Granada', 'Carrera del Darro', 4, 240000, 'usado', True, True, 'casa', 0, 'Vistas a la Alhambra', 'norte', False],
    ['gonzalo@example.com', 95, 'Valladolid', 'Valladolid', 'Paseo Zorrilla', 11, 175000, 'nuevo', False, False, 'apartamento', 2, 'Muy luminoso', 'este', True],
    ['carmen@example.com', 180, 'Málaga', 'Málaga', 'Calle Larios', 3, 290000, 'usado', True, True, 'piso', 6, 'Totalmente equipado', 'oeste', True],
    ['jorge@example.com', 105, 'Salamanca', 'Salamanca', 'Gran Vía', 7, 195000, 'nuevo', False, True, 'estudio', 1, 'Ideal para estudiantes', 'sur', True],
    ['natalia@example.com', 75, 'Toledo', 'Toledo', 'Calle Comercio', 13, 160000, 'usado', False, False, 'loft', 0, 'Encanto histórico', 'norte', False],
    ['miguel@example.com', 125, 'Pamplona', 'Navarra', 'Avenida Carlos III', 6, 205000, 'nuevo', True, False, 'dúplex', 3, 'Acabados de lujo', 'este', True],
    ['diana@example.com', 115, 'Murcia', 'Murcia', 'Calle Trapería', 14, 215000, 'usado', True, True, 'bungalow', 0, 'Céntrico y con terraza', 'oeste', False],
    ['oscar@example.com', 135, 'Santander', 'Cantabria', 'Paseo Pereda', 16, 225000, 'nuevo', False, True, 'apartamento', 4, 'Frente al mar', 'sur', True],
    ['patricia@example.com', 145, 'Lugo', 'Lugo', 'Rúa Nova', 17, 235000, 'usado', True, False, 'casa', 0, 'Ambiente rústico', 'norte', False],
    ['roberto@example.com', 155, 'Ourense', 'Ourense', 'Calle Progreso', 18, 245000, 'nuevo', True, True, 'chalet', 0, 'Moderno y espacioso', 'este', True]
]


def register():
    url = "http://127.0.0.1:7770/register"

    print("Registrando")
    print("-----------------------------------------------------------------")
    for i in usuarios:
        response = requests.post(url,json={"name":i[0],"email":i[1],"passw":i[2],"phone":i[3]},verify=False)   
        if(response.ok):
            print("Succes register: "+i[0])
        else:
            print("Failed register: "+i[0])

def login():
    url = "http://127.0.0.1:7770/login"

    print("Logeando ")
    print("-----------------------------------------------------------------")
    for i in usuarios:
        response = requests.post(url,json={"email":i[1],"passw":i[2]},verify=False)   
        print(response.content)
        if(response.ok):
            print("Succes login: "+i[0])
        else:
            print("Failed login: "+i[0])




def insertCasa():
    try:
        token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBydWViYUBnbWFpbC5jb20iLCJwcmVtaXVtIjpmYWxzZSwiZXhwIjoxNzE1ODc5NDI1fQ.ZB7ZIxqVy_9bFHTz3inQF7l3jr4azFH6azeiXdDYEckqL0XKUSx4aPvN06xxihbS9Hd1-A3yr_AMyqhE7nlaMw"

        propiedad_json = {
            "metrosCuadrados": 120,
            "ciudad": "Ciudad Ficticia",
            "provincia": "Provincia Ficticia",
            "calle": "Calle Ficticia",
            "numero": 123,
            "precio": 200000,
            "estado": "Excelente",
            "parking": True,
            "piscina": False,
            "tipoPropiedad": "Casa",
            "planta": 2,
            "descripcion": "Hermosa casa en una ubicación céntrica, con amplios espacios y excelente iluminación natural.",
            "habitacion": "3",
            "bano": "2",
            "orientacion": "Este",
            "ascensor": False
        }

        url = "https://127.0.0.1:7770/property"
        file_paths = ["pruebas1.webp", "pruebas2.webp"]
        files = [("files", open(file_path, "rb")) for file_path in file_paths]
        # Aquí convertimos el JSON en una cadena y lo añadimos al formulario como un campo de texto
        data = {"propiedad_json": json.dumps(propiedad_json)}
 
        headers = {"Authorization": f"{token}"}

        response = requests.post(url, data=data, files=files, headers=headers, verify=False)

        # Cerrar archivos
        for _, file in files:
            file.close()

        print(response.status_code)
        print(response.json())

    except Exception as e:
        print("Ocurrió un error:", e)
        if hasattr(e, 'response'):
            print(e.response.content)

def mandaUnarchivo():
    try:
        # URL del endpoint
        url = "http://127.0.0.1:7770/property/uploadimage"

        token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBydWViYUBnbWFpbC5jb20iLCJwcmVtaXVtIjpmYWxzZSwiZXhwIjoxNzE2NjQyNTU1fQ.uxrW8jTLVAEjB5mMdDwFDq75sao6CzxS-Z560sRGAtqdpb06h35Djm60Yqm573RO1iSggYazm9mPeGZJur_dAQ"
        # Lista de archivos a adjuntar
        file_paths = ["pruebas1.webp", "pruebas2.webp"]

        # Crear una lista de tuplas (nombre del campo, objeto de archivo)
        files = [("files", open(file_path, "rb")) for file_path in file_paths]
        header = {"Authorization": f"{token}"}  

        # Realizar la solicitud POST
        with requests.post(url, files=files, headers=header) as response:
            # Imprimir la respuesta
            print("Código de estado:", response.status_code)
            print("Respuesta:", response.json())
        
        # Cerrar archivos manualmente después de enviar la petición
        for _, file in files:
            file.close()

    except requests.exceptions.RequestException as e:
        print("Ocurrió un error en la solicitud:", e)
        if hasattr(e, 'response') and e.response:
            print("Contenido del error:", e.response.content)
    except Exception as e:
        print("Ocurrió un error:", e)

def getPropiedad():
    url = "http://127.0.0.1:7770/archivos"

    try:
        token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBydWViYUBnbWFpbC5jb20iLCJwcmVtaXVtIjpmYWxzZSwiZXhwIjoxNzE2NjQyMTQ2fQ.v_lAGSrMPqutc7Qz8LVSYxGGs8gyL1LhfV2Uer6elf_ny2jrLujeMBpjV2AwZ0BEw9bVe6IhB4VCa5eQbGpgWA"

        url = "https://127.0.0.1:7770/property"
 
        headers = {"Authorization": f"{token}"}


    
        for i in range(0,20):
            response = requests.get(url,headers=headers, verify=False)
            print(response.status_code)
            print(response.json())


        print(response.status_code)
        print(response.json())

    except Exception as e:
        print("Ocurrió un error:", e)
        if hasattr(e, 'response'):
            print(e.response.content)


register()
login()
#insertCasa()   
#getPropiedad()


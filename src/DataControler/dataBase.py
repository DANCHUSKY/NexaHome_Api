import os
from dotenv import load_dotenv
import psycopg2
import src.models.secure as secure
from src.models.UserModel import UserLoged,UserRegisted
from src.models.PropiedadModel import Propiedad


class DataBase:
    def __init__(self):
        load_dotenv()  # Cargar variables de entorno desde .env si existe

        # Obtener las variables de entorno o establecer valores predeterminados
        self.database_name = os.getenv("DATABASE_NAME")
        self.user = os.getenv("DATABASE_USER")
        self.password = os.getenv("DATABASE_PASSWORD")
        self.host = os.getenv("DATABASE_HOST")
        self.port = os.getenv("DATABASE_PORT")

    def obtener_conexion(self):
        # Crear y devolver una nueva conexión
        return psycopg2.connect(
            dbname=self.database_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def crear_tabla(self):
        # Crear una tabla llamada 'usuarios' con dos columnas: nombre y contraseña
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS usuarios (
                        nombre TEXT PRIMARY KEY,
                        contrasena TEXT NOT NULL
                    )
                ''')
                conexion.commit()

    def insertar_usuario(self,user: UserRegisted):
        # Insertar un nuevo usuario en la tabla

        salt = secure.encrypt(user.passw)
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('INSERT INTO usuario (nombre, correo, contrasena, salt, telefono) VALUES (%s,%s,%s,%s,%s)', (user.name,user.email,salt[0],salt[1],str(user.phone)))
                conexion.commit()

    def insert_property(self, correo: str, property: Propiedad):
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                insert_query = """
                INSERT INTO propiedad (
                    correo, 
                    metroscuadrados, 
                    ciudad, 
                    provincia, 
                    calle, 
                    numero, 
                    precio, 
                    estado, 
                    parking, 
                    piscina, 
                    tipopropiedad, 
                    planta, 
                    descripcion, 
                    orientacion, 
                    ascensor, 
                    habitaciones, 
                    banos
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) RETURNING id;
                """
                cursor.execute(insert_query, (
                    correo, 
                    property.metrosCuadrados, 
                    property.ciudad, 
                    property.provincia, 
                    property.calle, 
                    property.numero, 
                    property.precio, 
                    property.estado, 
                    't' if property.parking else 'f', 
                    't' if property.piscina else 'f', 
                    property.tipoPropiedad, 
                    property.planta, 
                    property.descripcion, 
                    property.orientacion, 
                    't' if property.ascensor else 'f', 
                    property.habitacion, 
                    property.bano
                ))
                inserted_id = cursor.fetchone()[0]
                conexion.commit()
                return inserted_id

    def eliminar_usuario(self, usuario_id):
        # Eliminar un usuario por nombre (ID no se utiliza en el esquema original)
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('DELETE FROM usuario WHERE nombre = %s', (usuario_id,))
                conexion.commit()

    def usuario_es_de_pago(self, usuario_correo):
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('SELECT correo FROM clientepremium WHERE correo = %s', (usuario_correo,))
                mailServer = cursor.fetchall()

                if(mailServer):
                    if(mailServer[0][0] == usuario_correo):
                        return True
                    else:
                        return False
                    
                else:
                    return False

    def obtener_usuarios(self):
        # Obtener todos los usuarios de la tabla
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('SELECT * FROM usuario')
                conexion.commit()
                
                return cursor.fetchall()

    def usuario_exist(self, email: str):
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('SELECT * FROM usuario WHERE correo = %s', (email,))
                conexion.commit()

                result = cursor.fetchall()
                
                if(result):
                    return True
                else:
                    return False
                
                    
    def getPropertysCount(self, email: str):
        # Eliminar un usuario por nombre (ID no se utiliza en el esquema original)
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('SELECT COUNT(*) FROM propiedad WHERE correo = %s', (email,))
                conexion.commit()

                return cursor.fetchone()[0]  
                
            
    def getMyPropertys(self, email: str):
        # Eliminar un usuario por nombre (ID no se utiliza en el esquema original)
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('SELECT * FROM propiedad WHERE correo = %s', (email,))
                conexion.commit()

                return cursor.fetchall()
            
    def getPropertyInRange(self,position: int):
        # Eliminar un usuario por nombre (ID no se utiliza en el esquema original)
        with self.obtener_conexion() as conexion:
            limit = 10
            with conexion.cursor() as cursor:
                cursor.execute('SELECT * FROM propiedad Limit %s OFFSET %s', (limit,position))
                conexion.commit()

                return cursor.fetchall()

    def getCountProperty(self):
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('SELECT count(*) FROM propiedad')
                conexion.commit()

                return cursor.fetchall()
            
    def getPropertyById(self, id: str):
        # Eliminar un usuario por nombre (ID no se utiliza en el esquema original)
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('SELECT * FROM propiedad WHERE id = %s', (id,))
                conexion.commit()

                return cursor.fetchall()
    
    def getPropertyByCity(self, ciudad: str):
        print("Ciudad del user: "+str(ciudad))
        # Eliminar un usuario por nombre (ID no se utiliza en el esquema original)
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('SELECT * FROM propiedad WHERE ciudad = %s', (ciudad,))
                conexion.commit()

                return cursor.fetchall()

    def getEmailProperty(self,id: int):
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('SELECT correo FROM propiedad WHERE id = %s', (id,))
                conexion.commit()

                email = cursor.fetchall()[0][0]
                return email
            
    def getUserName(self, email: str):
        # Eliminar un usuario por nombre (ID no se utiliza en el esquema original)
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('SELECT nombre FROM usuario WHERE correo = %s', (email,))
                conexion.commit()

                name = cursor.fetchall()[0][0]
                return name
    
    def getUserPhone(self, email: str):
        # Eliminar un usuario por nombre (ID no se utiliza en el esquema original)
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('SELECT telefono FROM usuario WHERE correo = %s', (email,))
                conexion.commit()

                phone = cursor.fetchall()[0][0]
                return phone
            
    def getUserPass(self, email: str):
        # Eliminar un usuario por nombre (ID no se utiliza en el esquema original)
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('SELECT contrasena FROM usuario WHERE correo = %s', (email,))
                conexion.commit()

                phone = cursor.fetchall()[0][0]
                return phone
    
    def getUserSalt(self, email: str):
        # Eliminar un usuario por nombre (ID no se utiliza en el esquema original)
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('SELECT salt FROM usuario WHERE correo = %s', (email,))
                conexion.commit()

                phone = cursor.fetchall()[0][0]
                return phone
            
    def PropertyExist(self, id: int):
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('SELECT count(*) FROM propiedad WHERE id = %s', (id,))
                conexion.commit()
                if(cursor.fetchall()[0][0] >= 1):
                    return True
                else:
                    return False
                
    def IsMyProperty(self, id: int,email: str):
        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('SELECT count(*) FROM propiedad WHERE id = %s and correo = %s', (id,email,))
                conexion.commit()
                if(cursor.fetchall()[0][0] >= 1):
                    return True
                else:
                    return False
                

    def changeUserPass(self, newPass: str, email: str):

        data = secure.encrypt(newPass)

        with self.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute('UPDATE usuario SET contrasena = %s , salt = %s WHERE  correo = %s', (data[0],data[1],email,))
                conexion.commit()
                


    
# Recuerda cambiar los valores de `database_name`, `user`, `password`, y `host` con los de tu configuración.

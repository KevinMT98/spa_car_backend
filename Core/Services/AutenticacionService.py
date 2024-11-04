from Core.Models.UserModel import UserModel
from utilidades import config
import csv
import hashlib

class AuthService:
    users = []

    @classmethod
    def cargar_usuarios(cls):
        cls.users.clear()
        try:
            with open(config.USERS_DB_PATH, newline='\n') as df:
                reader = csv.reader(df, delimiter=';')
                for username, password, rol in reader:
                    user = UserModel(username=username, password=password, rol=rol)
                    cls.users.append(user)
        except FileNotFoundError:
            print(f"Error: El archivo {config.USERS_DB_PATH} no se encontró.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")

    @classmethod
    def registrar_usuario(cls, user: UserModel):
        cls.cargar_usuarios()
        for u in cls.users:
            if u.username == user.username:
                return f"Error: El usuario {user.username} ya existe."

        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
        user.password = hashed_password

        try:
            with open(config.USERS_DB_PATH, mode='a', newline='\n') as df:
                writer = csv.writer(df, delimiter=';')
                writer.writerow([user.username, user.password, user.rol])
        except Exception as e:
            return f"Error al escribir en el archivo: {e}"

        cls.users.append(user)
        return f"Usuario {user.username} registrado exitosamente."

    @classmethod
    def verificar_credenciales(cls, username: str, password: str):
        cls.cargar_usuarios()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        for user in cls.users:
            if user.username == username and user.password == hashed_password:
                return True
        return False
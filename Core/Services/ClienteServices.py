from Core.Models.ClienteModel import Cliente
from utilidades import config 
import csv

class ClientesServices:
    lista = []

    @classmethod
    def cargar_datos(cls):
        try:
            with open(config.DATABASE_PATH, newline='\n') as df:
                reader = csv.reader(df, delimiter=';')
                for cedula, nombre, apellido, fec_nacimiento, telefono, correo_electronico in reader:
                    cliente = Cliente(cedula, nombre, apellido, fec_nacimiento, telefono, correo_electronico)
                    cls.lista.append(cliente)
        except FileNotFoundError:
            print(f"Error: El archivo {config.DATABASE_PATH} no se encontró.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")

    @classmethod
    def buscar(self, cedula):
        ClientesServices.cargar_datos()
        for cliente in self.lista:
            if cliente.cedula == cedula:
                return cliente
        return None

    @classmethod
    def agregar(self, cliente):
        self.lista.append(cliente)

    @classmethod
    def actualizar(self, cliente):
        for i, c in enumerate(self.lista):
            if c.cedula == cliente.cedula:
                self.lista[i] = cliente
                return
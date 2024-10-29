from ProyectoSPA.Core.Models import ClienteModel as Cliente
from utilidades import config
import csv

class Clientes:
    lista = []

    @classmethod
    def cargar_datos(self):
        try:
            with open(config.DATABASE_PATH, newline='\n') as df:
                reader = csv.reader(df, delimiter=';')
                for cedula, Nombre, apellido, Fec_nacimiento, telefono, correo_electornico in reader:
                    cliente = Cliente(cedula, Nombre, apellido, Fec_nacimiento, telefono, correo_electornico)
                    self.lista.append(cliente)
        except FileNotFoundError:
            print(f"Error: El archivo {config.DATABASE_PATH} no se encontró.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")

    @classmethod
    def buscar(self, cedula):
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
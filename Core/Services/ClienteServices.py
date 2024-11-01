from Core.Models.ClienteModel import Cliente, ClienteModel
from utilidades import config 
import csv

class ClientesServices:
    lista = []

    @classmethod
    def cargar_datos(cls):
        cls.lista.clear()
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
    def agregar(cls, cliente: ClienteModel):
        cls.cargar_datos()
        for cliente in cls.lista:
            if cliente.cedula == cliente.cedula:
                return f"Error: El cliente con la cédula {cliente.cedula} ya existe."
            else:
                with open(config.DATABASE_PATH, mode='a', newline='\n') as df:
                    writer = csv.writer(df, delimiter=';')
                    writer.writerow([cliente.cedula, cliente.nombre, cliente.apellido,
                             cliente.fec_nacimiento, cliente.telefono, cliente.correo_electronico])
                    cls.lista.append(cliente)
                    return f"Cliente con cédula {cliente.cedula} agregado exitosamente."
    
    @classmethod
    def actualizar(self, cliente):
        for i, c in enumerate(self.lista):
            if c.cedula == cliente.cedula:
                self.lista[i] = cliente
                return
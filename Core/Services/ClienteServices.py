from Core.Models.ClienteModel import Cliente, ClienteModel
from utilidades import config 
import csv
#
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
    def buscar(cls, cedula):
        cls.cargar_datos()
        for cliente in cls.lista:
            if cliente.cedula == cedula:
                return cliente
        return None

    @classmethod
    def agregar(cls, cliente: ClienteModel):
        cls.cargar_datos()
        for c in cls.lista:
            if c.cedula == cliente.cedula:
                return f"Error: El cliente con la cédula {cliente.cedula} ya existe."
        
        try:
            with open(config.DATABASE_PATH, mode='a', newline='\n') as df:
                writer = csv.writer(df, delimiter=';')
                writer.writerow([cliente.cedula, cliente.nombre, cliente.apellido,
                                 cliente.fec_nacimiento, cliente.telefono, cliente.correo_electronico])
        except Exception as e:
            return f"Error al escribir en el archivo: {e}"
        
        cls.lista.append(cliente)
        return f"Cliente {cliente.nombre} {cliente.apellido} agregado exitosamente."
    
    @classmethod
    def actualizar(cls, cliente: ClienteModel):
        cls.cargar_datos()
        for i, c in enumerate(cls.lista):
            if c.cedula == cliente.cedula:
                cls.lista[i] = cliente
                try:
                    with open(config.DATABASE_PATH, mode='w', newline='\n') as df:
                        writer = csv.writer(df, delimiter=';')
                        for cliente in cls.lista:
                            writer.writerow([cliente.cedula, cliente.nombre, cliente.apellido,
                                             cliente.fec_nacimiento, cliente.telefono, cliente.correo_electronico])
                    return f"Cliente {cliente.nombre} {cliente.apellido} actualizado exitosamente."
                except Exception as e:
                    return f"Error al escribir en el archivo: {e}"
        return f"Error: El cliente con la cédula {cliente.cedula} no existe."
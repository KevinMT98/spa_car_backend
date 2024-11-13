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
                for tipo_doc,documento, nombre, apellido, fec_nacimiento, telefono, email in reader:
                    cliente = Cliente(tipo_doc, documento, nombre, apellido, fec_nacimiento, telefono, email)
                    cls.lista.append(cliente)
        except FileNotFoundError:
            print(f"Error: El archivo {config.DATABASE_PATH} no se encontró.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")

    @classmethod
    def buscar(cls, documento):
        cls.cargar_datos()
        for cliente in cls.lista:
            if cliente.documento == documento:
                return cliente
        return None

    @classmethod
    def agregar(cls, cliente: ClienteModel):
        cls.cargar_datos()
        cliente.nombre = cliente.nombre.capitalize()
        cliente.apellido = cliente.apellido.capitalize()
        for c in cls.lista:
            if c.documento == cliente.documento:
                return f"Error: El cliente con la cédula {cliente.documento} ya existe."
        
        try:
            with open(config.DATABASE_PATH, mode='a', newline='\n') as df:
                writer = csv.writer(df, delimiter=';')
                writer.writerow([cliente.tipo_doc,cliente.documento, cliente.nombre, cliente.apellido,
                                 cliente.fec_nacimiento, cliente.telefono, cliente.email])
        except Exception as e:
            return f"Error al escribir en el archivo: {e}"
        
        cls.lista.append(cliente)
        return f"Cliente {cliente.nombre} {cliente.apellido} agregado exitosamente."
    
    @classmethod
    def actualizar(cls, cliente: ClienteModel):
        cls.cargar_datos()
        for i, c in enumerate(cls.lista):
            if c.documento == cliente.documento:
                cls.lista[i] = cliente
                try:
                    with open(config.DATABASE_PATH, mode='w', newline='\n') as df:
                        writer = csv.writer(df, delimiter=';')
                        for cliente in cls.lista:
                            writer.writerow([cliente.tipo_doc,cliente.documento, cliente.nombre, cliente.apellido,
                                             cliente.fec_nacimiento, cliente.telefono, cliente.email])
                    return f"Cliente {cliente.nombre} {cliente.apellido} actualizado exitosamente."
                except Exception as e:
                    return f"Error al escribir en el archivo: {e}"
        return f"Error: El cliente con la cédula {cliente.documento} no existe."
from Core.Models.ServicioModel import Servicio, ServicioModel
from utilidades import config
import csv
from decimal import Decimal

class ServiciosServices:
    lista = []

    @classmethod
    def cargar_datos(cls):
        cls.lista.clear()
        try:
            with open(config.SERVICIOS_DB_PATH, newline='\n') as df:
                reader = csv.reader(df, delimiter=';')
                for id_servicio, nombre, descripcion, precio_base, tipo_vehiculo, descuento, precio_variable in reader:
                    servicio = Servicio(
                        id_servicio, 
                        nombre, 
                        descripcion, 
                        Decimal(precio_base), 
                        tipo_vehiculo, 
                        Decimal(descuento),
                        precio_variable.lower() == 'true'
                    )
                    cls.lista.append(servicio)
        except FileNotFoundError:
            print(f"Error: El archivo {config.SERVICIOS_DB_PATH} no se encontró.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")

    @classmethod
    def buscar(cls, id_servicio: str):
        cls.cargar_datos()
        for servicio in cls.lista:
            if servicio.id_servicio == id_servicio:
                return servicio
        return None
    
    @classmethod
    def buscar_por_tipo_vehiculo(cls, tipo_vehiculo: str):
        cls.cargar_datos()
        return [servicio for servicio in cls.lista if servicio.tipo_vehiculo == tipo_vehiculo]

    @classmethod
    def agregar(cls, servicio: ServicioModel):
        cls.cargar_datos()
        for s in cls.lista:
            if s.id_servicio == servicio.id_servicio:
                return f"Error: El servicio con ID {servicio.id_servicio} ya existe."
        
        try:
            with open(config.SERVICIOS_DB_PATH, mode='a', newline='\n') as df:
                writer = csv.writer(df, delimiter=';')
                writer.writerow([
                    servicio.id_servicio, 
                    servicio.nombre, 
                    servicio.descripcion,
                    servicio.precio_base,
                    servicio.tipo_vehiculo,
                    servicio.descuento,
                    servicio.precio_variable
                ])
        except Exception as e:
            return f"Error al escribir en el archivo: {e}"
        
        cls.lista.append(servicio)
        return f"Servicio {servicio.nombre} agregado exitosamente."

    @classmethod
    def actualizar(cls, servicio: ServicioModel):
        cls.cargar_datos()
        for i, s in enumerate(cls.lista):
            if s.id_servicio == servicio.id_servicio:
                cls.lista[i] = servicio
                try:
                    with open(config.SERVICIOS_DB_PATH, mode='w', newline='\n') as df:
                        writer = csv.writer(df, delimiter=';')
                        for s in cls.lista:
                            writer.writerow([
                                s.id_servicio, 
                                s.nombre, 
                                s.descripcion,
                                str(s.precio_base),
                                s.tipo_vehiculo,
                                str(s.descuento),
                                str(s.precio_variable)
                            ])
                    return f"Servicio {servicio.nombre} actualizado exitosamente."
                except Exception as e:
                    return f"Error al escribir en el archivo: {e}"
        return f"Error: El servicio con ID {servicio.id_servicio} no existe."

    @classmethod
    def eliminar(cls, id_servicio: str):
        cls.cargar_datos()
        for i, servicio in enumerate(cls.lista):
            if servicio.id_servicio == id_servicio:
                cls.lista.pop(i)
                try:
                    with open(config.SERVICIOS_DB_PATH, mode='w', newline='\n') as df:
                        writer = csv.writer(df, delimiter=';')
                        for s in cls.lista:
                            writer.writerow([
                                s.id_servicio, 
                                s.nombre, 
                                s.descripcion,
                                str(s.precio_base),
                                s.tipo_vehiculo,
                                str(s.descuento),
                                str(s.precio_variable)
                            ])
                    return f"Servicio con ID {id_servicio} eliminado exitosamente."
                except Exception as e:
                    return f"Error al escribir en el archivo: {e}"
        return f"Error: El servicio con ID {id_servicio} no existe."

from Core.Models.VehiculoModel import VehiculoModel,Vehiculo
from utilidades import config
import csv

class VehiculoServices:
    lista = []

    @classmethod
    def cargar_datos(cls):
        cls.lista.clear()
        try:
            with open(config.VEHICULOS_DB_PATH, newline='\n') as df:
                reader = csv.reader(df, delimiter=';')
                for id_vehiculo, tipo_vehiculo, marca, modelo, cilindrada, tipo, cedula_cliente in reader:
                    vehiculo = Vehiculo(
                        id_vehiculo=id_vehiculo,
                        tipo_vehiculo=tipo_vehiculo,
                        marca=marca,
                        modelo=modelo,
                        cilindrada=int(cilindrada),
                        tipo=tipo,
                        cedula_cliente=cedula_cliente
                    )
                    cls.lista.append(vehiculo)
        except FileNotFoundError:
            print(f"Error: El archivo {config.VEHICULOS_DB_PATH} no se encontró.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")

    @classmethod
    def agregar(cls, vehiculo: VehiculoModel):
        cls.cargar_datos()
        vehiculo.id_vehiculo = vehiculo.id_vehiculo.upper()
        for v in cls.lista:
            if v.id_vehiculo == vehiculo.id_vehiculo:
                return f"Error: El vehículo con la placa {vehiculo.id_vehiculo} ya existe."

        try:
            with open(config.VEHICULOS_DB_PATH, mode='a', newline='\n') as df:
                writer = csv.writer(df, delimiter=';')
                writer.writerow([
                    vehiculo.id_vehiculo,
                    vehiculo.tipo_vehiculo,
                    vehiculo.marca,
                    vehiculo.modelo,
                    vehiculo.cilindrada,
                    vehiculo.tipo,
                    vehiculo.cedula_cliente
                ])
        except Exception as e:
            return f"Error al escribir en el archivo: {e}"

        cls.lista.append(vehiculo)
        return f"Vehículo {vehiculo.id_vehiculo} agregado exitosamente."

    @classmethod
    def actualizar(cls, vehiculo: VehiculoModel):
        cls.cargar_datos()
        for i, v in enumerate(cls.lista):
            if v.id_vehiculo == vehiculo.id_vehiculo:
                cls.lista[i] = vehiculo
                try:
                    with open(config.VEHICULOS_DB_PATH, mode='w', newline='\n') as df:
                        writer = csv.writer(df, delimiter=';')
                        for veh in cls.lista:
                            writer.writerow([
                                veh.id_vehiculo,
                                veh.tipo_vehiculo,
                                veh.marca,
                                veh.modelo,
                                veh.cilindrada,
                                veh.tipo,
                                veh.cedula_cliente
                            ])
                    return f"Vehículo {vehiculo.id_vehiculo} actualizado exitosamente."
                except Exception as e:
                    return f"Error al escribir en el archivo: {e}"
        return f"Error: El vehículo con la placa {vehiculo.id_vehiculo} no existe."

    @classmethod
    def eliminar(cls, id_vehiculo: str):
        id_vehiculo = id_vehiculo.upper()
        cls.cargar_datos()
        for i, v in enumerate(cls.lista):
            if v.id_vehiculo == id_vehiculo:
                del cls.lista[i]
                try:
                    with open(config.VEHICULOS_DB_PATH, mode='w', newline='\n') as df:
                        writer = csv.writer(df, delimiter=';')
                        for veh in cls.lista:
                            writer.writerow([
                                veh.id_vehiculo,
                                veh.tipo_vehiculo,
                                veh.marca,
                                veh.modelo,
                                veh.cilindrada,
                                veh.tipo,
                                veh.cedula_cliente
                            ])
                    return f"Vehículo con placa {id_vehiculo} eliminado exitosamente."
                except Exception as e:
                    return f"Error al escribir en el archivo: {e}"
        return f"Error: El vehículo con la placa {id_vehiculo} no existe."

    @classmethod
    def buscar(cls, id_vehiculo: str):
        cls.cargar_datos()
        id_vehiculo = id_vehiculo.upper()
        for vehiculo in cls.lista:
            if vehiculo.id_vehiculo == id_vehiculo:
                return vehiculo
        return None
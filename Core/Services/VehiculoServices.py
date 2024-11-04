import csv
from Core.Models.VehiculoModel import VehiculoModel
from utilidades import config

class VehiculoServices:
    lista = []

    @classmethod
    def cargar_datos(cls):
        cls.lista.clear()
        try:
            with open(config.VEHICULOS_DB_PATH, newline='\n') as df:
                reader = csv.reader(df, delimiter=';')
                for row in reader:
                    vehiculo = VehiculoModel(
                        id_vehiculo=row[0],
                        tipo_vehiculo=row[1],
                        marca=row[2],
                        modelo=row[3],
                        cilindrada=int(row[4]),
                        tipo=row[5],
                        cedula_cliente=row[6]
                    )
                    cls.lista.append(vehiculo)
        except FileNotFoundError:
            print(f"Error: El archivo {config.VEHICULOS_DB_PATH} no se encontró.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")

    @classmethod
    def agregar(cls, vehiculo: VehiculoModel):
        cls.cargar_datos()
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
        for vehiculo in cls.lista:
            if vehiculo.id_vehiculo == id_vehiculo:
                return vehiculo
        return None
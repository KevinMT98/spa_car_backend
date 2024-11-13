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
                for placa, documento_cliente, segmento, marca,linea, modelo, cilindrada, tipo in reader:
                    vehiculo = Vehiculo(
                        placa=placa,
                        documento_cliente=documento_cliente,
                        segmento=segmento,
                        marca=marca,
                        linea=linea,
                        modelo=modelo,
                        cilindrada = cilindrada,
                        tipo=tipo
                        
                    )
                    cls.lista.append(vehiculo)
        except FileNotFoundError:
            print(f"Error: El archivo {config.VEHICULOS_DB_PATH} no se encontró.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")

    @classmethod
    def agregar(cls, vehiculo: VehiculoModel):
        cls.cargar_datos()
        vehiculo.placa = vehiculo.placa.upper()
        vehiculo.marca = vehiculo.marca.capitalize()
        vehiculo.linea = vehiculo.linea.upper()
        for v in cls.lista:
            if v.placa == vehiculo.placa:
                return f"Error: El vehículo con la placa {vehiculo.placa} ya existe."

        try:
            with open(config.VEHICULOS_DB_PATH, mode='a', newline='\n') as df:
                writer = csv.writer(df, delimiter=';')
                writer.writerow([
                    vehiculo.placa,
                    vehiculo.documento_cliente,
                    vehiculo.segmento,
                    vehiculo.marca,
                    vehiculo.linea,
                    vehiculo.modelo,
                    vehiculo.cilindrada,
                    vehiculo.tipo,                    
                ])
        except Exception as e:
            return f"Error al escribir en el archivo: {e}"

        cls.lista.append(vehiculo)
        return f"Vehículo {vehiculo.placa} agregado exitosamente."

    @classmethod
    def actualizar(cls, vehiculo: VehiculoModel):
        cls.cargar_datos()
        for i, v in enumerate(cls.lista):
            if v.placa == vehiculo.placa:
                cls.lista[i] = vehiculo
                try:
                    with open(config.VEHICULOS_DB_PATH, mode='w', newline='\n') as df:
                        writer = csv.writer(df, delimiter=';')
                        for veh in cls.lista:
                            writer.writerow([
                                veh.placa,
                                veh.documento_cliente,
                                veh.segmento,
                                veh.marca,
                                veh.linea,
                                veh.modelo,
                                veh.cilindrada,
                                veh.tipo,
                                
                            ])
                    return f"Vehículo {vehiculo.placa} actualizado exitosamente."
                except Exception as e:
                    return f"Error al escribir en el archivo: {e}"
        return f"Error: El vehículo con la placa {vehiculo.placa} no existe."

    @classmethod
    def eliminar(cls, placa: str):
        placa = placa.upper()
        cls.cargar_datos()
        for i, v in enumerate(cls.lista):
            if v.placa == placa:
                del cls.lista[i]
                try:
                    with open(config.VEHICULOS_DB_PATH, mode='w', newline='\n') as df:
                        writer = csv.writer(df, delimiter=';')
                        for veh in cls.lista:
                            writer.writerow([
                                veh.placa,
                                veh.documento_cliente,
                                veh.segmento,
                                veh.marca,
                                veh.linea,
                                veh.modelo,
                                veh.cilindrada,
                                veh.tipo,
                                
                            ])
                    return f"Vehículo con placa {placa} eliminado exitosamente."
                except Exception as e:
                    return f"Error al escribir en el archivo: {e}"
        return f"Error: El vehículo con la placa {placa} no existe."

    @classmethod
    def buscar_placa(cls, placa: str):
        cls.cargar_datos()
        placa = placa.upper()
        for vehiculo in cls.lista:
            if vehiculo.placa == placa:
                return vehiculo
        return None
    
    @classmethod
    def buscar_cliente(cls, documento_cliente: str):
        cls.cargar_datos()
        documento_cliente = documento_cliente
        for vehiculo in cls.lista:
            if vehiculo.documento_cliente == documento_cliente:
                return vehiculo
        return None
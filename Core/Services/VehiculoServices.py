from Core.Models.VehiculoModel import VehiculoModel, Vehiculo
from utilidades import config
import csv
import os

class VehiculoServices:
    lista = []
    COLUMNAS_CSV = [
        'PLACA', 'DOCUMENTO_CLIENTE', 'CATEGORIA', 'SEGMENTO','MARCA',
        'LINEA', 'MODELO', 'CILINDRADA', 'GRUPO'
    ]

    @classmethod
    def cargar_datos(cls):
        cls.lista.clear()
        try:
            if not os.path.exists(config.VEHICULOS_DB_PATH):
                # Crear archivo con encabezados si no existe
                with open(config.VEHICULOS_DB_PATH, 'w', newline='\n',encoding="utf-8") as df:
                    writer = csv.writer(df, delimiter=';')
                    writer.writerow(cls.COLUMNAS_CSV)
                return

            with open(config.VEHICULOS_DB_PATH, newline='\n',encoding="utf-8") as df:
                reader = csv.DictReader(df, delimiter=';', fieldnames=cls.COLUMNAS_CSV)
                next(reader)  # Saltar encabezados
                for row in reader:
                    vehiculo = Vehiculo(
                        placa=row['PLACA'],
                        documento_cliente=row['DOCUMENTO_CLIENTE'],
                        categoria=row['CATEGORIA'],
                        segmento=row['SEGMENTO'],
                        marca=row['MARCA'],
                        linea=row['LINEA'],
                        modelo=row['MODELO'],
                        cilindrada=row['CILINDRADA'],
                        grupo=row['GRUPO']
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
        
        if any(v.placa == vehiculo.placa for v in cls.lista):
            return f"Error: El vehículo con la placa {vehiculo.placa} ya existe."
        
        try:
            archivo_existe = os.path.exists(config.VEHICULOS_DB_PATH)
            modo = 'a' if archivo_existe else 'w'
            
            with open(config.VEHICULOS_DB_PATH, mode=modo, newline='\n',encoding="utf-8") as df:
                writer = csv.DictWriter(df, fieldnames=cls.COLUMNAS_CSV, delimiter=';')
                if not archivo_existe:
                    writer.writeheader()
                
                writer.writerow({
                    'PLACA': vehiculo.placa,
                    'DOCUMENTO_CLIENTE': vehiculo.documento_cliente,
                    'CATEGORIA': vehiculo.categoria,
                    'SEGMENTO': vehiculo.segmento,
                    'MARCA': vehiculo.marca,
                    'LINEA': vehiculo.linea,
                    'MODELO': vehiculo.modelo,
                    'CILINDRADA': vehiculo.cilindrada,
                    'GRUPO': vehiculo.grupo
                })
            
            cls.lista.append(vehiculo)
            return f"Vehículo {vehiculo.placa} agregado exitosamente."
        except Exception as e:
            return f"Error al escribir en el archivo: {e}"

    @classmethod
    def actualizar(cls, vehiculo: VehiculoModel):
        cls.cargar_datos()
        for i, v in enumerate(cls.lista):
            if v.placa == vehiculo.placa:
                cls.lista[i] = vehiculo
                try:
                    with open(config.VEHICULOS_DB_PATH, mode='w', newline='\n',encoding="utf-8") as df:
                        writer = csv.DictWriter(df, fieldnames=cls.COLUMNAS_CSV, delimiter=';')
                        writer.writeheader()
                        for veh in cls.lista:
                            writer.writerow({
                                'PLACA': veh.placa,
                                'DOCUMENTO_CLIENTE': veh.documento_cliente,
                                'CATEGORIA': veh.categoria,
                                'SEGMENTO': veh.segmento,
                                'MARCA': veh.marca,
                                'LINEA': veh.linea,
                                'MODELO': veh.modelo,
                                'CILINDRADA': veh.cilindrada,
                                'GRUPO': veh.grupo
                            })
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
                    with open(config.VEHICULOS_DB_PATH, mode='w', newline='\n',encoding="utf-8") as df:
                        writer = csv.DictWriter(df, fieldnames=cls.COLUMNAS_CSV, delimiter=';')
                        writer.writeheader()
                        for veh in cls.lista:
                            writer.writerow({
                                'PLACA': veh.placa,
                                'DOCUMENTO_CLIENTE': veh.documento_cliente,
                                'CATEGORIA': veh.categoria,
                                'SEGMENTO': veh.segmento,
                                'MARCA': veh.marca,
                                'LINEA': veh.linea,
                                'MODELO': veh.modelo,
                                'CILINDRADA': veh.cilindrada,
                                'GRUPO': veh.grupo
                            })
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
        vehiculos_cliente = [vehiculo for vehiculo in cls.lista if vehiculo.documento_cliente == documento_cliente]
        return vehiculos_cliente if vehiculos_cliente else None
from Core.Models.ServicioModel import ServicioGeneralModel, ServicioAdicionalModel, CategoriaValor, GrupoValor
from utilidades import config
import csv
import os
import json

class ServiciosServices:
    lista_generales = []
    lista_adicionales = []
    COLUMNAS_GENERALES = ['ID_SERVICIO', 'NOMBRE', 'TIPO_SERVICIO', 'CATEGORIA', 'GRUPO', 'PRECIO']
    COLUMNAS_ADICIONALES = ['ID_SERVICIO', 'NOMBRE', 'TIPO_SERVICIO', 'CATEGORIA', 'PRECIO_VARIABLE', 'VARIABLE', 'PRECIO_BASE']

    @classmethod
    def _obtener_ultimo_id(cls, archivo, id_inicial):
        if not os.path.exists(archivo):
            return id_inicial
        
        try:
            with open(archivo, 'r', newline='') as df:
                reader = csv.DictReader(df, delimiter=';')
                ids = [int(row['ID_SERVICIO']) for row in reader]
                return max(ids) + 1 if ids else id_inicial
        except:
            return id_inicial

    @classmethod
    def agregarGeneral(cls, servicio: ServicioGeneralModel):
        try:
            archivo_existe = os.path.exists(config.SERVICIOS_GENERALES_DB_PATH)
            modo = 'a' if archivo_existe else 'w'
            
            with open(config.SERVICIOS_GENERALES_DB_PATH, mode=modo, newline='\n') as df:
                writer = csv.DictWriter(df, fieldnames=cls.COLUMNAS_GENERALES, delimiter=';')
                if not archivo_existe:
                    writer.writeheader()
                
                for valor in servicio.valores:
                    for grupo in valor.grupos:
                        nuevo_id = cls._obtener_ultimo_id(config.SERVICIOS_GENERALES_DB_PATH, 1001)
                        writer.writerow({
                            'ID_SERVICIO': str(nuevo_id),
                            'NOMBRE': servicio.nombre,
                            'TIPO_SERVICIO': servicio.tipo_servicio,
                            'CATEGORIA': valor.categoria,
                            'GRUPO': grupo.id,
                            'PRECIO': grupo.precio
                        })
            
            return f"Servicio {servicio.nombre} guardado exitosamente."
        except Exception as e:
            return f"Error al guardar servicio general: {e}"

    @classmethod
    def agregarAdicional(cls, servicio: ServicioAdicionalModel):
        try:
            archivo_existe = os.path.exists(config.SERVICIOS_ADICIONALES_DB_PATH)
            modo = 'a' if archivo_existe else 'w'
            
            with open(config.SERVICIOS_ADICIONALES_DB_PATH, mode=modo, newline='\n') as df:
                writer = csv.DictWriter(df, fieldnames=cls.COLUMNAS_ADICIONALES, delimiter=';')
                if not archivo_existe:
                    writer.writeheader()
                
                for categoria in servicio.categorias:
                    nuevo_id = cls._obtener_ultimo_id(config.SERVICIOS_ADICIONALES_DB_PATH, 5001)
                    writer.writerow({
                        'ID_SERVICIO': str(nuevo_id),
                        'NOMBRE': servicio.nombre,
                        'TIPO_SERVICIO': servicio.tipo_servicio,
                        'CATEGORIA': categoria,
                        'PRECIO_VARIABLE': servicio.precio_variable,
                        'VARIABLE': servicio.variable,
                        'PRECIO_BASE': servicio.precio_base
                    })
            
            return f"Servicio {servicio.nombre} guardado exitosamente."
        except Exception as e:
            return f"Error al guardar servicio adicional: {e}"

from Core.Models.ServicioModel import ServicesModel, CategoriaValor, GrupoValor, Servicio
from utilidades import config
import csv
import os
import json

class ServiciosServices:
    lista = []
    COLUMNAS_CSV = ['ID_SERVICIO', 'NOMBRE', 'TIPO_SERVICIO', 'VALORES']

    @classmethod
    def cargar_datos(cls):
        cls.lista.clear()
        try:
            if not os.path.exists(config.SERVICIOS_DB_PATH):
                with open(config.SERVICIOS_DB_PATH, 'w', newline='\n') as df:
                    writer = csv.writer(df, delimiter=';')
                    writer.writerow(cls.COLUMNAS_CSV)
                return

            with open(config.SERVICIOS_DB_PATH, 'r', newline='\n') as df:
                reader = csv.DictReader(df, delimiter=';')
                for row in reader:
                    valores = json.loads(row['VALORES'])
                    categorias = [
                        CategoriaValor(
                            categoria=cat['categoria'],
                            grupos=[GrupoValor(**grupo) for grupo in cat['grupos']]
                        )
                        for cat in valores
                    ]
                    
                    servicio = ServicesModel(
                        id_servicio=row['ID_SERVICIO'],
                        nombre=row['NOMBRE'],
                        tipo_servicio=row['TIPO_SERVICIO'],
                        valores=categorias
                    )
                    cls.lista.append(servicio)

        except Exception as e:
            print(f"Error al cargar datos: {str(e)}")
            return False

    @classmethod
    def agregar(cls, servicio: ServicesModel):
        cls.cargar_datos()
        
        if any(s.id_servicio == servicio.id_servicio for s in cls.lista):
            return f"Error: El servicio con ID {servicio.id_servicio} ya existe."

        try:
            archivo_existe = os.path.exists(config.SERVICIOS_DB_PATH)
            modo = 'a' if archivo_existe else 'w'
           
            with open(config.SERVICIOS_DB_PATH, mode=modo, newline='\n') as df:
                writer = csv.DictWriter(df, fieldnames=cls.COLUMNAS_CSV, delimiter=';')
                if not archivo_existe:
                    writer.writeheader()
                
                writer.writerow({
                    'ID_SERVICIO': servicio.id_servicio,
                    'NOMBRE': servicio.nombre,
                    'TIPO_SERVICIO': servicio.tipo_servicio,
                    'VALORES': json.dumps([cat.model_dump() for cat in servicio.valores])
                })
                
                cls.lista.append(servicio)
            return True
        except Exception as e:
            print(f"Error al guardar servicio: {str(e)}")
            return False

    @classmethod
    def obtener_todos(cls):
        cls.cargar_datos()
        return cls.lista

    @classmethod
    def obtener_por_id(cls, id_servicio):
        cls.cargar_datos()
        return next((servicio for servicio in cls.lista if servicio.id_servicio == id_servicio), None)
    
    @classmethod
    def obtener_por_categoria(cls, categoria):
        cls.cargar_datos()
        return [servicio for servicio in cls.lista if servicio.categoria == categoria]

    @classmethod
    def actualizar(cls, servicio: ServicesModel):
        cls.cargar_datos()
        indice = next((i for i, s in enumerate(cls.lista) if s.id_servicio == servicio.id_servicio), -1)
        
        if indice == -1:
            return False

        cls.lista[indice] = servicio
        return cls._guardar_lista()

    @classmethod
    def eliminar(cls, id_servicio):
        cls.cargar_datos()
        servicio = cls.obtener_por_id(id_servicio)
        
        if not servicio:
            return False

        cls.lista = [s for s in cls.lista if s.id_servicio != id_servicio]
        return cls._guardar_lista()

    @classmethod
    def _guardar_lista(cls):
        try:
            with open(config.SERVICIOS_DB_PATH, 'w', newline='\n') as df:
                writer = csv.DictWriter(df, fieldnames=cls.COLUMNAS_CSV, delimiter=';')
                writer.writeheader()
                for servicio in cls.lista:
                    writer.writerow({
                        'ID_SERVICIO': servicio.id_servicio,
                        'NOMBRE': servicio.nombre,
                        'TIPO_SERVICIO': servicio.tipo_servicio,
                        'VALORES': json.dumps([cat.model_dump() for cat in servicio.valores])
                    })
            return True
        except Exception as e:
            print(f"Error al guardar lista: {str(e)}")
            return False

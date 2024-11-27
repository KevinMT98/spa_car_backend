from Core.Models.ServicioModel import ServicioGeneralModel, ServicioAdicionalModel, CategoriaValor, GrupoValor
from utilidades import config
from utilidades.config import SERVICIOS_ADICIONALES_DB_PATH, SERVICIOS_GENERALES_DB_PATH
import csv
import os


class ServiciosServices:
    lista_generales = []
    lista_adicionales = []
    COLUMNAS_GENERALES = ['ID_SERVICIO', 'NOMBRE', 'TIPO_SERVICIO', 'CATEGORIA', 'GRUPO', 'PRECIO']
    COLUMNAS_ADICIONALES = ['ID_SERVICIO', 'NOMBRE', 'TIPO_SERVICIO', 'CATEGORIA', 'PRECIO_VARIABLE', 'VARIABLE', 'PRECIO_BASE']
    
    ID_SERVICIO_GENERAL = 1000
    @classmethod
    def _obtener_ultimo_id_general(cls):
        if not os.path.exists(SERVICIOS_GENERALES_DB_PATH):
            return cls.ID_SERVICIO_GENERAL
        
        try:
            with open(SERVICIOS_GENERALES_DB_PATH, 'r', newline='', encoding="utf-8") as df:
                reader = csv.DictReader(df, delimiter=';')
                ids = set([int(row['ID_SERVICIO']) for row in reader])
                return max(ids) + 1 if ids else cls.ID_SERVICIO_GENERAL
        except:
            return cls.ID_SERVICIO_GENERAL
        
    ID_SERVICIO_ADICIONAL = 5000
    @classmethod
    def _obtener_ultimo_id_adicional(cls):
        if not os.path.exists(SERVICIOS_ADICIONALES_DB_PATH):
            return cls.ID_SERVICIO_ADICIONAL
        
        try:
            with open(SERVICIOS_ADICIONALES_DB_PATH, 'r', newline='', encoding="utf-8") as df:
                reader = csv.DictReader(df, delimiter=';')
                ids = set([int(row['ID_SERVICIO']) for row in reader])
                return max(ids) + 1 if ids else cls.ID_SERVICIO_ADICIONAL
        except:
            return cls.ID_SERVICIO_ADICIONAL

    @classmethod
    def _servicio_existe(cls, archivo, nombre):
        if not os.path.exists(archivo):
            return False
        
        try:
            with open(archivo, 'r', newline='',encoding="utf-8") as df:
                reader = csv.DictReader(df, delimiter=';')
                for row in reader:
                    if row['NOMBRE'] == nombre:
                        return True
            return False
        except:
            return False

    @classmethod
    def agregarGeneral(cls, servicio: ServicioGeneralModel):
        try:
            if cls._servicio_existe(config.SERVICIOS_GENERALES_DB_PATH, servicio.nombre):
                return f"Error: El servicio general con nombre '{servicio.nombre}' ya existe."
            
            archivo_existe = os.path.exists(config.SERVICIOS_GENERALES_DB_PATH)
            modo = 'a' if archivo_existe else 'w'
            
            # Obtener un único ID para todo el servicio
            id_servicio = cls._obtener_ultimo_id_general()
            
            with open(config.SERVICIOS_GENERALES_DB_PATH, mode=modo, newline='\n',encoding="utf-8") as df:
                writer = csv.DictWriter(df, fieldnames=cls.COLUMNAS_GENERALES, delimiter=';')
                if not archivo_existe:
                    writer.writeheader()
                
                for valor in servicio.valores:
                    for grupo in valor.grupos:
                        writer.writerow({
                            'ID_SERVICIO': str(id_servicio),  # Mismo ID para todos los registros del servicio
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
            if cls._servicio_existe(config.SERVICIOS_ADICIONALES_DB_PATH, servicio.nombre):
                return f"Error: El servicio adicional con nombre '{servicio.nombre}' ya existe."
            
            archivo_existe = os.path.exists(config.SERVICIOS_ADICIONALES_DB_PATH)
            modo = 'a' if archivo_existe else 'w'
            
            # Obtener un único ID para todo el servicio
            id_servicio = cls._obtener_ultimo_id_adicional()
            
            with open(config.SERVICIOS_ADICIONALES_DB_PATH, mode=modo, newline='\n',encoding="utf-8") as df:
                writer = csv.DictWriter(df, fieldnames=cls.COLUMNAS_ADICIONALES, delimiter=';')
                if not archivo_existe:
                    writer.writeheader()
                
                for categoria in servicio.categorias:
                    writer.writerow({
                        'ID_SERVICIO': str(id_servicio),
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

    @classmethod
    def _ensure_csv_exists(cls, archivo, columnas):
        if not os.path.exists(archivo):
            with open(archivo, 'w', newline='', encoding="utf-8") as df:
                writer = csv.DictWriter(df, fieldnames=columnas, delimiter=';')
                writer.writeheader()

    @classmethod
    def _ordenar_y_guardar_registros(cls, archivo, columnas, rows):
        rows_ordenados = sorted(rows, key=lambda x: int(x['ID_SERVICIO']))
        with open(archivo, 'w', newline='', encoding="utf-8") as df:
            writer = csv.DictWriter(df, fieldnames=columnas, delimiter=';')
            writer.writeheader()
            writer.writerows(rows_ordenados)

    @classmethod
    def consultar_todos(cls, tipo_servicio):
        archivo = config.SERVICIOS_GENERALES_DB_PATH if tipo_servicio == 'general' else config.SERVICIOS_ADICIONALES_DB_PATH
        columnas = cls.COLUMNAS_GENERALES if tipo_servicio == 'general' else cls.COLUMNAS_ADICIONALES
        cls._ensure_csv_exists(archivo, columnas)

        try:
            servicios_dict = {}
            with open(archivo, 'r', newline='', encoding="utf-8") as df:
                reader = csv.DictReader(df, delimiter=';')
                for row in reader:
                    servicio_id = row['NOMBRE']  # Agrupar por nombre del servicio
                    if servicio_id not in servicios_dict:
                        servicios_dict[servicio_id] = {
                            'nombre': row['NOMBRE'],
                            'tipo_servicio': row['TIPO_SERVICIO'],
                            'valores' if tipo_servicio == 'general' else 'categorias': []
                        }
                    
                    if tipo_servicio == 'general':
                        valor = {
                            'categoria': row['CATEGORIA'],
                            'grupo': row['GRUPO'],
                            'precio': row['PRECIO']
                        }
                        servicios_dict[servicio_id]['valores'].append(valor)
                    else:
                        categoria = {
                            'categoria': row['CATEGORIA'],
                            'precio_variable': row['PRECIO_VARIABLE'],
                            'variable': row['VARIABLE'],
                            'precio_base': row['PRECIO_BASE']
                        }
                        servicios_dict[servicio_id]['categorias'].append(categoria)

            return list(servicios_dict.values())
        except Exception as e:
            return f"Error al consultar servicios: {e}"

    @classmethod
    def update_servicio(cls, servicio_id, servicio, tipo_servicio):
        try:
            archivo = config.SERVICIOS_GENERALES_DB_PATH if tipo_servicio == 'general' else config.SERVICIOS_ADICIONALES_DB_PATH
            columnas = cls.COLUMNAS_GENERALES if tipo_servicio == 'general' else cls.COLUMNAS_ADICIONALES
            cls._ensure_csv_exists(archivo, columnas)

            rows = []
            servicio_encontrado = False
            
            # Obtener registros existentes excluyendo el servicio a actualizar
            with open(archivo, 'r', newline='', encoding="utf-8") as df:
                reader = csv.DictReader(df, delimiter=';')
                for row in reader:
                    if str(row['ID_SERVICIO']) == str(servicio_id):
                        servicio_encontrado = True
                    else:
                        rows.append(row)

            if not servicio_encontrado:
                return "Error: Servicio no encontrado"

            # Crear nuevos registros
            nuevos_registros = []
            if tipo_servicio == 'general':
                for valor in servicio.valores:
                    for grupo in valor.grupos:
                        nuevo_registro = {
                            'ID_SERVICIO': servicio_id,
                            'NOMBRE': servicio.nombre,
                            'TIPO_SERVICIO': servicio.tipo_servicio,
                            'CATEGORIA': valor.categoria,
                            'GRUPO': grupo.id,
                            'PRECIO': grupo.precio
                        }
                        nuevos_registros.append(nuevo_registro)
            else:
                for categoria in servicio.categorias:
                    nuevo_registro = {
                        'ID_SERVICIO': servicio_id,
                        'NOMBRE': servicio.nombre,
                        'TIPO_SERVICIO': servicio.tipo_servicio,
                        'CATEGORIA': categoria,
                        'PRECIO_VARIABLE': servicio.precio_variable,
                        'VARIABLE': servicio.variable,
                        'PRECIO_BASE': servicio.precio_base
                    }
                    nuevos_registros.append(nuevo_registro)

            rows.extend(nuevos_registros)
            cls._ordenar_y_guardar_registros(archivo, columnas, rows)
            return servicio
        except Exception as e:
            return f"Error al actualizar servicio: {str(e)}"

    @classmethod
    def delete_servicio(cls, servicio_id, tipo_servicio):
        archivo = config.SERVICIOS_GENERALES_DB_PATH if tipo_servicio == 'general' else config.SERVICIOS_ADICIONALES_DB_PATH
        columnas = cls.COLUMNAS_GENERALES if tipo_servicio == 'general' else cls.COLUMNAS_ADICIONALES
        cls._ensure_csv_exists(archivo, columnas)

        try:
            rows = []
            deleted = False
            with open(archivo, 'r', newline='', encoding="utf-8") as df:
                reader = csv.DictReader(df, delimiter=';')
                total_rows = 0
                for row in reader:
                    total_rows += 1
                    if str(row['ID_SERVICIO']) != str(servicio_id):
                        rows.append(row)
                deleted = len(rows) < total_rows

            if not deleted:
                raise ValueError("Servicio no encontrado")

            cls._ordenar_y_guardar_registros(archivo, columnas, rows)
            return True
        except Exception as e:
            return f"Error al eliminar servicio: {e}"

    @classmethod
    def consultar_por_id(cls, tipo_servicio, id_servicio):
        archivo = config.SERVICIOS_GENERALES_DB_PATH if tipo_servicio.lower() == 'general' else config.SERVICIOS_ADICIONALES_DB_PATH
        columnas = cls.COLUMNAS_GENERALES if tipo_servicio.lower() == 'general' else cls.COLUMNAS_ADICIONALES
        cls._ensure_csv_exists(archivo, columnas)

        try:
            servicio_dict = None
            valores = []
            
            with open(archivo, 'r', newline='', encoding="utf-8") as df:
                reader = csv.DictReader(df, delimiter=';')
                for row in reader:
                    if int(row['ID_SERVICIO']) == int(id_servicio):
                        if servicio_dict is None:
                            servicio_dict = {
                                'id_servicio': row['ID_SERVICIO'],
                                'nombre': row['NOMBRE'],
                                'tipo_servicio': row['TIPO_SERVICIO'],
                                'valores' if tipo_servicio.lower() == 'general' else 'categorias': []
                            }
                        
                        if tipo_servicio.lower() == 'general':
                            valor = {
                                'categoria': row['CATEGORIA'],
                                'grupos': [{
                                    'id': row['GRUPO'],
                                    'precio': row['PRECIO']
                                }]
                            }
                            categoria_existente = next(
                                (item for item in valores if item['categoria'] == row['CATEGORIA']), 
                                None
                            )
                            if categoria_existente:
                                categoria_existente['grupos'].append(valor['grupos'][0])
                            else:
                                valores.append(valor)
                        else:
                            valor = {
                                'categoria': row['CATEGORIA'],
                                'precio_variable': row['PRECIO_VARIABLE'],
                                'variable': row['VARIABLE'],
                                'precio_base': row['PRECIO_BASE']
                            }
                            valores.append(valor)

            if servicio_dict:
                servicio_dict['valores' if tipo_servicio.lower() == 'general' else 'categorias'] = valores
                return servicio_dict
            return None
            
        except Exception as e:
            return f"Error al consultar servicio por ID: {e}"

    @classmethod
    def consultar_por_nombre(cls, tipo_servicio, nombre):
        archivo = config.SERVICIOS_GENERALES_DB_PATH if tipo_servicio == 'general' else config.SERVICIOS_ADICIONALES_DB_PATH
        if not os.path.exists(archivo):
            return None

        try:
            with open(archivo, 'r', newline='',encoding="utf-8") as df:
                reader = csv.DictReader(df, delimiter=';')
                for row in reader:
                    if row['NOMBRE'] == nombre:
                        return row
            return None
        except Exception as e:
            return f"Error al consultar servicio por nombre: {e}"


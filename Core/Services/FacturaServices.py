import csv
import os
import json
from datetime import timezone, datetime
from Core.Models.FacturaModel import Factura
from utilidades.config import FACTURAS_DB_PATH

class FacturaServices:
    lista = []
    COLUMNAS_CSV = [
        'factura', 'fecha', 'placa', 'categoria','grupo','cliente', 
        'medio_pago', 'descuento', 'vlr_descuento', 'subtotal', 'total', 'servicios',
        'cantidad', 'descripcion', 'valor'
    ]
    NUMERO_INICIAL_FACTURA = 10000

    @classmethod
    def _ensure_csv_exists(cls):
        if not os.path.exists(FACTURAS_DB_PATH):
            with open(FACTURAS_DB_PATH, 'w', newline='', encoding="utf-8") as df:
                writer = csv.DictWriter(df, fieldnames=cls.COLUMNAS_CSV, delimiter=';')
                writer.writeheader()

    @classmethod
    def _obtener_ultimo_id(cls):
        if not os.path.exists(FACTURAS_DB_PATH):
            return cls.NUMERO_INICIAL_FACTURA
        
        try:
            with open(FACTURAS_DB_PATH, 'r', newline='') as df:
                reader = csv.DictReader(df, delimiter=';')
                ids = set([int(row['factura']) for row in reader])  # Usar set para obtener números únicos
                return max(ids) + 1 if ids else cls.NUMERO_INICIAL_FACTURA
        except:
            return cls.NUMERO_INICIAL_FACTURA

    @classmethod
    def get_all(cls):
        cls._ensure_csv_exists()
        try:
            facturas_dict = {}  # Diccionario para agrupar servicios por factura
            
            with open(FACTURAS_DB_PATH, 'r', newline='', encoding="utf-8") as df:
                reader = csv.DictReader(df, delimiter=';')
                
                for row in reader:
                    factura_id = row['factura']
                    
                    if factura_id not in facturas_dict:
                        # Convertir la fecha al formato deseado
                        fecha_str = row['fecha']
                        try:
                            # Intentar parsear la fecha ISO
                            fecha_dt = datetime.fromisoformat(fecha_str)
                            # Convertir a formato YYYY-MM-DD
                            fecha_formatted = fecha_dt.date().isoformat()
                        except ValueError:
                            # Si falla, mantener la fecha original
                            fecha_formatted = fecha_str

                        facturas_dict[factura_id] = {
                            'factura': int(row['factura']),
                            'fecha': fecha_formatted,  # Usar la fecha formateada
                            'placa': row['placa'],
                            'categoria': row['categoria'],
                            'grupo': int(row['grupo']),
                            'cliente': row['cliente'],
                            'medio_pago': row['medio_pago'],
                            'descuento': float(row['descuento']),
                            'vlr_descuento': float(row['vlr_descuento']),
                            'subtotal': float(row['subtotal']),
                            'total': float(row['total']),
                            'servicios': []
                        }
                    
                    # Agregar servicio a la factura existente
                    servicio = {
                        'servicio': int(row['servicios']),
                        'cantidad': int(row['cantidad']),
                        'descripcion': row['descripcion'],
                        'valor': float(row['valor']),
                    }
                    facturas_dict[factura_id]['servicios'].append(servicio)
            
            return list(facturas_dict.values())
            
        except Exception as e:
            return f"Error al consultar facturas: {e}"

    @classmethod
    def get_by_id(cls, factura_id: int):
        cls._ensure_csv_exists()
        try:
            with open(FACTURAS_DB_PATH, 'r', newline='', encoding="utf-8") as df:
                reader = csv.DictReader(df, delimiter=';')
                factura = None
                servicios = []
                for row in reader:
                    if int(row['factura']) == factura_id:
                        if factura is None:
                            factura = cls._process_row(row)
                        servicio = {
                            'servicio': int(row['servicios']),
                            'cantidad': int(row['cantidad']),
                            'descripcion': row['descripcion'],
                            'valor': float(row['valor']),
                        }
                        servicios.append(servicio)
                if factura:
                    factura['servicios'] = servicios
                return factura
            return None
        except Exception as e:
            return f"Error al consultar factura: {e}"

    @classmethod
    def _ordenar_y_guardar_registros(cls, rows):
        """Ordena los registros por número de factura y los guarda en el archivo"""
        # Ordenar registros por número de factura
        rows_ordenados = sorted(rows, key=lambda x: int(x['factura']))
        
        # Guardar registros ordenados
        with open(FACTURAS_DB_PATH, 'w', newline='', encoding="utf-8") as df:
            writer = csv.DictWriter(df, fieldnames=cls.COLUMNAS_CSV, delimiter=';')
            writer.writeheader()
            writer.writerows(rows_ordenados)

    @classmethod
    def create(cls, factura: Factura):
        cls._ensure_csv_exists()
        try:
            # Leer registros existentes
            existing_rows = []
            with open(FACTURAS_DB_PATH, 'r', newline='') as df:
                reader = csv.DictReader(df, delimiter=';')
                existing_rows = list(reader)

            # Obtener nuevo número de factura
            nuevo_numero = cls._obtener_ultimo_id()
            
            factura_base = {
                'factura': int(nuevo_numero),  # Usar el nuevo número autogenerado
                'fecha': factura.fecha.isoformat(),  # Updated format
                'placa': factura.placa.upper(),
                'categoria': factura.categoria.capitalize(),
                'grupo': int(factura.grupo),
                'cliente': factura.id_cliente,
                'medio_pago': factura.medio_pago.upper(),
                'descuento': float(factura.descuento),
                'vlr_descuento': float(factura.vlr_descuento),
                'subtotal': float(factura.subtotal),
                'total': float(factura.total),
            }
            
            # Crear nuevos registros
            nuevos_registros = []
            for servicio in factura.servicios:
                row = factura_base.copy()
                row.update({
                    'servicios': servicio.id_servicio,
                    'cantidad': servicio.cantidad,
                    'descripcion': servicio.descripcion,
                    'valor': float(servicio.valor),
                })
                nuevos_registros.append(row)
            
            # Combinar y ordenar todos los registros
            existing_rows.extend(nuevos_registros)
            cls._ordenar_y_guardar_registros(existing_rows)
            
            # Actualizar el número de factura en el objeto antes de devolverlo
            factura.numero_factura = nuevo_numero
            return factura.to_dict()
        except Exception as e:
            return f"Error al crear factura: {e}"

    @classmethod
    def update(cls, factura_id: int, factura: Factura):
        cls._ensure_csv_exists()
        rows = []
        
        try:
            # Verificar si la factura existe antes de actualizar
            if not cls.get_by_id(factura_id):
                raise ValueError("Factura no encontrada")

            # Leer todos los registros excepto los de la factura a actualizar
            with open(FACTURAS_DB_PATH, 'r', newline='') as df:
                reader = csv.DictReader(df, delimiter=';')
                rows = [row for row in reader if int(row['factura']) != factura_id]

            # Agregar los nuevos registros de la factura actualizada
            factura_base = {
                'factura': int(factura_id),
                'fecha': factura.fecha.astimezone(timezone.utc).isoformat(),  # Updated format
                'placa': factura.placa,
                'categoria': factura.categoria.capitalize(),
                'grupo': int(factura.grupo),
                'cliente': factura.id_cliente,
                'medio_pago': factura.medio_pago.upper(),
                'descuento': float(factura.descuento),
                'vlr_descuento': float(factura.vlr_descuento),
                'subtotal': float(factura.subtotal),
                'total': float(factura.total),
            }

            # Crear los nuevos registros para cada servicio
            nuevos_registros = []
            for servicio in factura.servicios:
                row = factura_base.copy()
                row.update({
                    'servicios': servicio.id_servicio,
                    'cantidad': servicio.cantidad,
                    'descripcion': servicio.descripcion,
                    'valor': float(servicio.valor),
                })
                nuevos_registros.append(row)

            if not nuevos_registros:
                raise ValueError("No hay servicios para actualizar en la factura")

            # Combinar y ordenar registros
            rows.extend(nuevos_registros)
            cls._ordenar_y_guardar_registros(rows)
            
            # Retornar la factura actualizada con todos sus servicios
            return {
                **factura_base,
                'servicios': [
                    {
                        'servicio': s.id_servicio,
                        'cantidad': s.cantidad,
                        'descripcion': s.descripcion,
                        'valor': float(s.valor),
                    } for s in factura.servicios
                ]
            }
        except ValueError as ve:
            raise ve
        except Exception as e:
            return f"Error al actualizar factura: {e}"

    @classmethod
    def delete(cls, factura_id: int):
        cls._ensure_csv_exists()
        rows = []
        deleted = False
        
        try:
            # Leer todas las filas excepto las que coinciden con factura_id
            with open(FACTURAS_DB_PATH, 'r', newline='') as df:
                reader = csv.DictReader(df, delimiter=';')
                total_rows = 0
                for row in reader:
                    total_rows += 1
                    if int(row['factura']) != factura_id:
                        rows.append(row)
                
                # Verificar si se encontraron filas para eliminar
                deleted = len(rows) < total_rows
            
            if not deleted:
                raise ValueError("Factura no encontrada")
            
            # Ordenar registros restantes antes de guardar
            cls._ordenar_y_guardar_registros(rows)
            
            return True
        except Exception as e:
            return f"Error al eliminar factura: {e}"

    @classmethod
    def _process_row(cls, row):
        """Procesa una fila del CSV para convertir en el formato requerido"""
        servicio = {
            'servicio': int(row['servicios']),
            'cantidad': int(row['cantidad']),
            'descripcion': row['descripcion'],
            'valor': float(row['valor']),
        }
        return {
            'factura': int(row['factura']),
            'fecha': row['fecha'],
            'placa': row['placa'],
            'categoria': row['categoria'],
            'grupo': int(row['grupo']),
            'cliente': row['cliente'],
            'medio_pago': row['medio_pago'],  # Asegurarse de usar la clave correcta del CSV
            'descuento': float(row['descuento']),
            'vlr_descuento': float(row['vlr_descuento']),
            'subtotal': float(row['subtotal']),
            'total': float(row['total']),
            'servicios': [servicio]
        }
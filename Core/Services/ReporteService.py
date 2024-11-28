from datetime import datetime
from typing import List, Dict
from Core.Models.FacturaModel import Factura
from Core.Services.FacturaServices import FacturaServices
from Core.Models.FacturaModel import Factura
import csv
import os

class ReporteServices:
    @classmethod
    def get_all(cls, fecha_inicio: str = None, fecha_fin: str = None):
        """
        Obtiene todas las facturas filtradas por rango de fecha.
        fecha_inicio y fecha_fin deben estar en formato 'YYYY-MM-DD'
        """
        try:
            # Obtener todas las facturas
            facturas = FacturaServices.get_all()
            
            if isinstance(facturas, str) and "Error" in facturas:
                return facturas
                
            # Si no hay fechas de filtro, retornar todas las facturas
            if not fecha_inicio or not fecha_fin:
                return facturas
                
            # Convertir fechas de filtro a datetime
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
            
            # Filtrar facturas por rango de fechas
            facturas_filtradas = []
            for factura in facturas:
                try:
                    # La fecha en el CSV está en formato YYYY-MM-DD, convertirla a datetime
                    fecha_factura_str = factura.get('fecha', '')
                    if fecha_factura_str:
                        fecha_factura = datetime.strptime(fecha_factura_str, '%Y-%m-%d')
                        # Verificar si la fecha está en el rango
                        if fecha_inicio_dt <= fecha_factura <= fecha_fin_dt:
                            facturas_filtradas.append(factura)
                except (ValueError, TypeError) as e:
                    continue  # Ignorar facturas con fechas inválidas
            
            return facturas_filtradas
            
        except Exception as e:
            return f"Error al procesar reporte: {str(e)}"

    @classmethod
    def get_by_numero_factura(cls, numero_factura: int):
        """
        Obtiene las facturas filtradas por número de factura.
        """
        try:
            # Obtener todas las facturas
            facturas = FacturaServices.get_all()
            
            if isinstance(facturas, str) and "Error" in facturas:
                return facturas
            
            # Filtrar facturas por número de factura
            facturas_filtradas = [factura for factura in facturas if int(factura['factura']) == numero_factura]
            
            return facturas_filtradas
            
        except Exception as e:
            return f"Error al procesar reporte: {str(e)}"
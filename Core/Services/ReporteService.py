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

    @classmethod
    def get_resumen(cls, fecha_inicio: str = None, fecha_fin: str = None):
        """
        Obtiene el resumen de ventas filtrado por rango de fecha.
        """
        try:
            # Obtener todas las facturas
            facturas = FacturaServices.get_all()
            
            if isinstance(facturas, str) and "Error" in facturas:
                return facturas
            
            # Filtrar facturas por rango de fechas si se proporcionan
            if fecha_inicio and fecha_fin:
                fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
                facturas = [
                    factura for factura in facturas
                    if fecha_inicio_dt <= datetime.strptime(factura['fecha'], '%Y-%m-%d') <= fecha_fin_dt
                ]
            
            # Inicializar resumen
            resumen = {
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "total_ventas": 0,
                "numero_facturas": 0,
                "ventas_medios_pago": [
                    {"medio_pago": "TR", "total_ventas": 0, "numero_facturas": 0},
                    {"medio_pago": "TD", "total_ventas": 0, "numero_facturas": 0},
                    {"medio_pago": "TC", "total_ventas": 0, "numero_facturas": 0},
                    {"medio_pago": "EF", "total_ventas": 0, "numero_facturas": 0}
                ],
                "ventas_diarias": []
            }
            
            # Calcular total de ventas y número de facturas
            resumen["total_ventas"] = sum(float(factura['valor']) for factura in facturas)
            resumen["numero_facturas"] = len(facturas)
            
            # Calcular ventas por medio de pago
            for medio in resumen["ventas_medios_pago"]:
                ventas_medio = [factura for factura in facturas if factura['medio_pago'] == medio["medio_pago"]]
                medio["total_ventas"] = sum(float(factura['valor']) for factura in ventas_medio)
                medio["numero_facturas"] = len(ventas_medio)
            
            # Calcular ventas diarias
            fechas = sorted(set(factura['fecha'] for factura in facturas))
            categorias = ["Moto", "Auto", "Cuatrimoto"]
            for fecha in fechas:
                ventas_fecha = [factura for factura in facturas if factura['fecha'] == fecha]
                ventas_diarias = {
                    "fecha": fecha,
                    "total_ventas": sum(float(factura['valor']) for factura in ventas_fecha),
                    "numero_facturas": len(ventas_fecha),
                    "categorias": []
                }
                for categoria in categorias:
                    ventas_categoria = [factura for factura in ventas_fecha if factura['categoria'] == categoria]
                    ventas_diarias["categorias"].append({
                        "categoria": categoria,
                        "total_ventas": sum(float(factura['valor']) for factura in ventas_categoria),
                        "numero_facturas": len(ventas_categoria)
                    })
                resumen["ventas_diarias"].append(ventas_diarias)
            
            return resumen
            
        except Exception as e:
            return f"Error al procesar resumen: {str(e)}"
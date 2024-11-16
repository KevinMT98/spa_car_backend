from Core.Models.ConfigModel import ConfigModel
from utilidades import config
import json
import os

class ConfigService:
    @classmethod
    def obtener_config(cls) -> ConfigModel:
        """Obtiene la configuración actual o crea una por defecto"""
        try:
            with open(config.CONFIG_FILE, 'r') as file:
                config_data = json.load(file)
                return ConfigModel(**config_data)
        except FileNotFoundError:
            default_config = cls._crear_config_default()
            cls.guardar_config(default_config)
            return default_config
        except Exception as e:
            print(f"Error al cargar configuración: {e}")
            return cls._crear_config_default()

    @classmethod
    def guardar_config(cls, config_data: ConfigModel) -> bool:
        """Guarda la configuración en archivo"""
        try:
            os.makedirs(os.path.dirname(config.CONFIG_FILE), exist_ok=True)
            with open(config.CONFIG_FILE, 'w') as file:
                json_data = config_data.dict()
                json.dump(json_data, file, indent=4)
            return True
        except Exception as e:
            print(f"Error guardando configuración: {e}")
            return False

    @classmethod
    def actualizar_config(cls, actualizaciones: dict) -> ConfigModel:
        """Actualiza parcialmente la configuración"""
        config_actual = cls.obtener_config()
        datos_actualizados = config_actual.dict()
        datos_actualizados.update(actualizaciones)
        nueva_config = ConfigModel(**datos_actualizados)
        cls.guardar_config(nueva_config)
        return nueva_config

    @classmethod
    def restablecer_config(cls) -> ConfigModel:
        """Restablece la configuración a valores por defecto"""
        config_default = cls._crear_config_default()
        cls.guardar_config(config_default)
        return config_default

    @staticmethod
    def _crear_config_default() -> ConfigModel:
        """Crea una configuración con valores por defecto"""
        return ConfigModel(
            empresa={
                "nombre": "SPA Car Service",
                "nit": "900000000-0",
                "telefono": "+57 1234567890", 
                "direccion": "Dirección por defecto",
                "logo": "assets/default-logo.png"
            },
            tema={
                "primario": "#007bff",
                "secondario": "#6c757d"
            }
        )
import json
import os
from Core.Models.ConfigModel import ConfigModel
from utilidades import config

class ConfigService:
    @classmethod
    def cargar_config(cls) -> ConfigModel:
        try:
            with open(config.CONFIG_FILE, 'r') as file:
                config_data = json.load(file)
                return ConfigModel(**config_data)
        except FileNotFoundError:
            default_config = cls.configuracion_estandar()
            cls.agregar(default_config)
            return default_config

    @classmethod
    def agregar(cls, configuracion: ConfigModel) -> bool:
        try:
            os.makedirs(os.path.dirnombre(config.CONFIG_FILE), exist_ok=True)
            with open(config.CONFIG_FILE, 'w') as file:
                json_data = configuracion.dict()
                json.dump(json_data, file, indent=4)
            return True
        except Exception as e:
            print(f"Error guardando configuración: {e}")
            return False

    @classmethod
    def modificar_config(cls, updates: dict) -> ConfigModel:
        current_config = cls.cargar_config()
        updated_data = current_config
        updated_data.update(updates)
        new_config = ConfigModel(**updated_data)
        cls.cargar_config(new_config)
        return new_config

    @staticmethod
    def configuracion_estandar() -> ConfigModel:
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
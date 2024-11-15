from pathlib import Path

# Obtén el directorio actual
BASE_DIR = Path(__file__).resolve().parent.parent

# Usa pathlib para construir la ruta
DATABASE_PATH = BASE_DIR / "DbContext" / "clientes.csv"
USERS_DB_PATH = BASE_DIR / "DbContext" / "usuarios.csv"
VEHICULOS_DB_PATH = BASE_DIR / "DbContext" /  "vehiculos.csv"
SERVICIOS_DB_PATH = BASE_DIR / "DbContext" /  "servicios.csv"
# CONFIG_FILE = BASE_DIR / "DbContext" / "config.json"
CONFIG_FILE = r'C:\ProyectoSPA\spa_car_backend\DbContext\config.json'

Headers = {"Content-Type": "application/json, charset=utf-8"}


# DATABASE_PATH = r'C:\ProyectoSPA\spa_car_backend\DbContext\clientes.csv'
# USERS_DB_PATH = r'C:\ProyectoSPA\spa_car_backend\DbContext\usuarios.csv'
# VEHICULOS_DB_PATH = r'C:\ProyectoSPA\spa_car_backend\DbContext\vehiculos.csv'
# SERVICIOS_DB_PATH = r'C:\ProyectoSPA\spa_car_backend\DbContext\servicios.csv'
# CONFIG_FILE = "DbContext/config.json"
# Headers = {"Content-Type": "application/json, charset=utf-8"}

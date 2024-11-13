# SPA Car Backend

Este proyecto es una API web para gestionar clientes de un servicio de SPA para autos. Está construido utilizando Python y Uvicorn.

## Estructura del Proyecto

- `main.py`: Punto de entrada de la aplicación.
- `ClienteModel.py`: Define el modelo de datos para los clientes.
- `ClienteServices.py`: Contiene los servicios para gestionar los datos de los clientes.
- `config.py`: Archivo de configuración que contiene rutas y otros parámetros de configuración.
- `utilidades.py`: Utilidades varias que ayudan en diferentes tareas del proyecto.
- `Web_API/Controllers/Cliente_controller.py`: Controlador que maneja las rutas y las solicitudes relacionadas con los clientes.
- `DbContext/clientes.csv`: Archivo CSV que almacena los datos de los clientes.

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clona el repositorio:

    ```sh
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd spa_car_backend
    ```

2. Crea y activa un entorno virtual:

    ```sh
    python -m venv venv
    venv\Scripts\activate  # En Windows
    # source venv/bin/activate  # En macOS y Linux
    ```

3. Instala las dependencias:

    ```sh
    pip install -r requirements.txt
    ```

## Uso

1. Ejecuta la aplicación:

    ```sh
    uvicorn main:app --reload
    ```

2. La API estará disponible en `http://127.0.0.1:8001`.

## Endpoints

- `GET /clientes/{cliente_id}`: Obtiene la información de un cliente por su ID.
- `POST /clientes/agregar/`: Agrega un nuevo cliente.

## Archivos Principales

### `ClienteModel.py`

Define la clase `Cliente` que representa a un cliente del servicio de SPA para autos.

```python
class Cliente:
    def __init__(self, documento, nombre, apellido, fec_nacimiento, telefono, email):
        self.documento = documento
        self.nombre = nombre
        self.apellido = apellido
        self.fec_nacimiento = fec_nacimiento
        self.telefono = telefono
        self.email = email

    def to_dict(self):
        return {
            "documento": self.documento,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fec_nacimiento": self.fec_nacimiento,
            "telefono": self.telefono,
            "email": self.email
        }
```

### `ClienteServices.py`

Contiene la clase `ClientesServices` que maneja la carga y búsqueda de datos de clientes.

```python
from Core.Models.ClienteModel import Cliente
from utilidades import config 
import csv

class ClientesServices:
    lista = []

    @classmethod
    def cargar_datos(cls):
        try:
            with open(config.DATABASE_PATH, newline='\n') as df:
                reader = csv.reader(df, delimiter=';')
                for documento, nombre, apellido, fec_nacimiento, telefono, email in reader:
                    cliente = Cliente(documento, nombre, apellido, fec_nacimiento, telefono, email)
                    cls.lista.append(cliente)
        except FileNotFoundError:
            print(f"Error: El archivo {config.DATABASE_PATH} no se encontró.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")

    @classmethod
    def buscar(self, documento):
        ClientesServices.cargar_datos()
        for cliente in self.lista:
            if cliente.documento == documento:
                return cliente
        return None
```

### `main.py`

Punto de entrada de la aplicación.

```python
from Web_API.Controllers.Cliente_controller import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
```

## Configuración

### `config.py`

Define las configuraciones necesarias para el proyecto, como la ruta a la base de datos.

```python
DATABASE_PATH = r'C:\ProyectoSPA\spa_car_backend\DbContext\clientes.csv'
Headers = {"Content-Type": "application/json, charset=utf-8"}
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría hacer.

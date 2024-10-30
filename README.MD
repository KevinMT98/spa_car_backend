# SPA Car Backend

Este proyecto es una API web para gestionar clientes de un servicio de SPA para autos. Está construido utilizando Python y Uvicorn.

## Estructura del Proyecto

- `main.py`: Punto de entrada de la aplicación.
- `ClienteModel.py`: Define el modelo de datos para los clientes.
- `ClienteServices.py`: Contiene los servicios para gestionar los datos de los clientes.
- `config.py`: Archivo de configuración que contiene rutas y otros parámetros de configuración.
- `utilidades.py`: Utilidades varias que pueden ser usadas en diferentes partes del proyecto.

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu_usuario/spa_car_backend.git
    cd spa_car_backend
    ```

2. Crea un entorno virtual y actívalo:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # En Windows
    source venv/bin/activate  # En Unix o MacOS
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Ejecución

Para ejecutar la aplicación, usa el siguiente comando:
```bash
python -m uvicorn main:app --reload
```

## Archivos Principales

### `ClienteModel.py`

Define la clase `Cliente` que representa a un cliente del servicio de SPA para autos.

```python
class Cliente:
    def __init__(self, cedula, nombre, apellido, fec_nacimiento, telefono, correo_electronico):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.fec_nacimiento = fec_nacimiento
        self.telefono = telefono
        self.correo_electronico = correo_electronico

    def to_dict(self):
        return {
            "cedula": self.cedula,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fec_nacimiento": self.fec_nacimiento,
            "telefono": self.telefono,
            "correo_electronico": self.correo_electronico
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
                for cedula, nombre, apellido, fec_nacimiento, telefono, correo_electronico in reader:
                    cliente = Cliente(cedula, nombre, apellido, fec_nacimiento, telefono, correo_electronico)
                    cls.lista.append(cliente)
        except FileNotFoundError:
            print(f"Error: El archivo {config.DATABASE_PATH} no se encontró.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")

    @classmethod
    def buscar(self, cedula):
        ClientesServices.cargar_datos()
        for cliente in self.lista:
            if cliente.cedula == cedula:
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
DATABASE_PATH = 'ruta/a/tu/base_de_datos.csv'
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría hacer.



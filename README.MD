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
- `tests/`: Directorio que contiene las pruebas del proyecto.
- `Web_API/Controllers/`: Directorio que contiene los controladores de la API.
- `Core/Models/`: Directorio que contiene los modelos de datos.
- `Core/Models/VehiculoModel.py`: Define el modelo de datos para los vehículos.
- `Core/Models/UserModel.py`: Define el modelo de datos para los usuarios.
- `Core/Models/ServicioModel.py`: Define el modelo de datos para los servicios.

## Modelos de Datos

### Vehículo
El modelo Vehículo representa los autos que ingresan al SPA:
- placa: Identificador único del vehículo
- marca: Marca del vehículo
- modelo: Modelo del vehículo
- año: Año de fabricación
- color: Color del vehículo
- propietario_id: ID del cliente propietario

### Servicio
Representa los servicios disponibles en el SPA:
- id: Identificador único del servicio
- nombre: Nombre del servicio
- descripcion: Descripción detallada
- precio: Costo del servicio
- duracion: Tiempo estimado del servicio

### Usuario
Define los usuarios del sistema:
- id: Identificador único
- usuario: Nombre de usuario
- rol: Rol en el sistema (admin/operador)
- estado: Estado del usuario (activo/inactivo)

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
- `PUT /clientes/actualizar/{cliente_id}`: Actualiza la información de un cliente existente.
- `DELETE /clientes/eliminar/{cliente_id}`: Elimina un cliente por su ID.

## Endpoints Adicionales

### Vehículos
- `GET /vehiculos/`: Lista todos los vehículos
- `GET /vehiculos/{placa}`: Obtiene un vehículo específico
- `POST /vehiculos/`: Registra un nuevo vehículo
- `PUT /vehiculos/{placa}`: Actualiza información del vehículo
- `DELETE /vehiculos/{placa}`: Elimina un vehículo

### Servicios
- `GET /servicios/`: Lista todos los servicios disponibles
- `GET /servicios/{id}`: Obtiene detalles de un servicio
- `POST /servicios/`: Crea un nuevo servicio
- `PUT /servicios/{id}`: Actualiza un servicio
- `DELETE /servicios/{id}`: Elimina un servicio

### Usuarios
- `POST /usuarios/login`: Autenticación de usuarios
- `POST /usuarios/registro`: Registro de nuevos usuarios
- `PUT /usuarios/{id}`: Actualización de datos de usuario
- `GET /usuarios/perfil`: Obtiene el perfil del usuario actual

### Configuración
- `GET /config/`: Obtiene la configuración actual del sistema
- `PATCH /config/`: Actualiza parcialmente la configuración
- `PUT /config/reset`: Restaura la configuración por defecto

## Manejo de Errores

La API maneja diferentes tipos de errores y devuelve respuestas adecuadas:

- `404 Not Found`: Cuando no se encuentra un cliente con el ID proporcionado.
- `400 Bad Request`: Cuando los datos proporcionados en la solicitud no son válidos.
- `500 Internal Server Error`: Cuando ocurre un error inesperado en el servidor.

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

if __nombre__ == "__main__":
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

## Seguridad
- Autenticación mediante JWT (JSON Web Tokens)
- Roles y permisos configurables
- Encriptación de contraseñas con bcrypt
- Validación de datos en todas las peticiones

## Configuración Avanzada

### Variables de Entorno

## Contribuciones


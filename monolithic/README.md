# Solución Monolítica - Laboratorio 1 MPI

## Descripción

Esta solución monolítica del Laboratorio 1 de Sistemas Distribuidos se centra en el uso de MPI para la implementación de un sistema de procesamiento de datos paralelo y distribuido. La solución monolítica integra todas las funcionalidades en un único despliegue, lo que facilita el desarrollo y la depuración pero puede limitar la escalabilidad en comparación con arquitecturas más desacopladas.

## Instrucciones de Uso

### Preparación del Entorno

1. **Instalación de Dependencias**: Asegúrate de que todas las dependencias necesarias estén instaladas ejecutando:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuración de Variables de Entorno**: Edita el archivo `.env` dentro de la carpeta `monolithic` para configurar los parámetros de conexión a la base de datos:
   ```env
   DB_USER=<user>
   DB_PASSWORD=<password>
   DB_HOST=<host>
   DB_PORT=<port>
   DB_NAME=<database>
   ```

### Ejecución del Programa

- Ejecuta la aplicación usando:
  ```bash
  python monolithic/app.py
  ```

- Después de iniciar el programa, el servidor se lanzará en el puerto 5000. Para acceder a la interfaz web, abre un navegador y visita `http://localhost:5000/`. La interfaz permite cargar, procesar y descargar archivos CSV, además de visualizar los resultados del procesamiento en formato JSON.

### Interacción Adicional

- Utiliza herramientas como Postman o Hoppscotch para realizar solicitudes POST y GET adicionales si prefieres interactuar con la API de forma programática en lugar de usar la interfaz gráfica.

## Componentes y Herramientas

- **Python**: 3.12.0
- **Flask**: Utilizado para el manejo del servidor web y la interfaz de usuario.
- **MPI4py**: Utilizado para el paralelismo y la distribución de procesos.
- **Pandas y Numpy**: Usados para la manipulación eficiente de datos.
- **PostgreSQL**: Sistema de gestión de bases de datos para almacenamiento persistente.
- **python-dotenv**: Utilizado para la carga de variables de entorno desde archivos `.env`.

Para más detalles sobre la instalación y configuración de dependencias, consulta la sección `Versiones` del documento principal del laboratorio.

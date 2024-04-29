# Solución Basada en Eventos - Laboratorio 1 MPI

## Descripción

La solución basada en eventos del Laboratorio 1 de Sistemas Distribuidos adopta un enfoque orientado a eventos para el procesamiento de datos. En este modelo, los servicios y componentes reaccionan a eventos específicos en lugar de solicitudes directas, lo que permite un alto grado de desacoplamiento y escalabilidad. Esta arquitectura es ideal para manejar flujos de datos en tiempo real y para sistemas donde la reactividad y la eficiencia en la comunicación son cruciales.

## Instrucciones de Uso

### Preparación del Entorno

1. **Instalación de Dependencias**: Instala las dependencias necesarias para que los manejadores de eventos y otros componentes funcionen correctamente. Desde la carpeta `event_driven`, ejecuta:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuración de Variables de Entorno**: Configura las variables de entorno en el archivo `.env` dentro de la carpeta `event_driven` para ajustar los parámetros de conexión y configuración de los servicios relacionados con el manejo de eventos:
   ```env
   DB_USER=<user>
   DB_PASSWORD=<password>
   DB_HOST=<host>
   DB_PORT=<port>
   DB_NAME=<database>
   ```

### Ejecución del Programa

- Utiliza MPI para lanzar el programa que gestiona y procesa los eventos. Por ejemplo:
  ```bash
  python event_driven/app.py
  ```

- Los servicios y procesadores de eventos estarán escuchando y reaccionando a los eventos generados, ya sea por fuentes internas o externas, procesando datos conforme llegan.

### Interacción con la Aplicación

- Aunque el sistema está orientado a eventos, se proporciona una interfaz web básica para interactuar con el sistema, disponible en `http://localhost:5000/`. Esta interfaz puede usarse para disparar eventos manualmente o para monitorizar el estado del sistema.

- Además, la solución permite la interacción programática mediante API REST o mediante la emisión directa de eventos a través de herramientas especializadas o scripts diseñados para tal efecto.

## Componentes y Herramientas

- **Flask**: Utilizado para levantar un servidor web sencillo que puede ser parte de la emisión o gestión de eventos.
- **MPI4py**: Fundamental para la gestión de procesos y la comunicación entre ellos en un entorno distribuido.
- **Pandas y Numpy**: Utilizados para el manejo eficiente de los datos dentro de los procesadores de eventos.
- **PostgreSQL**: Empleado para la persistencia de los resultados del procesamiento de eventos.
- **python-dotenv**: Utilizado para la carga de variables de entorno desde archivos `.env`.

Para detalles adicionales sobre las versiones de las herramientas y configuraciones específicas, consulta la sección `Versiones` del documento principal del laboratorio.


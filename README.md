# Laboratorio 1 - MPI
# Sistemas distribuidos

# Indice
- [General](#general)
- [Descripción](#descripción)
- [Instrucciones](#instrucciones)
- [Versiones](#versiones)

[//]: # (General)
[//]: # (Descripción)
[//]: # (Instrucciones)
[//]: # (Versiones)

## General

A continuación se detallan los aspectos generales del laboratorio.

- **Asignatura**: Sistemas Distribuidos
- **Laboratorio**: 1
- **Tema**: MPI
- **Fecha de entrega**: 2024-04-28
- **Integrantes**:
    - Nombre: [Carlos Retamales](https://github.com/CRetamales)
    - Nombre: [David Valero](https://github.com/DavidValeroCroma)
- **Profesor**: Manuel Ignacio Manríquez
- **Ayudante**: Ariel Madariaga
- **Carrera**: Ingeniería Civil en Informática
- **Universidad**: Universidad de Santiago de Chile (USACH) 🦁
- **Descripción**: Diseñar, implementar y comparar arquitecturas de cómputo paralelo distribuido utilizando herramientas como MPI para el procesamiento eficiente de datos.
- **Informe**: [Informe MPI](https://docs.google.com/document/d/19i7-_CRU4GGb5r72BVpdWXqw_OxHw37N4kM1AB9qAcE/edit?usp=sharing)
- **Enunciado**: [Enunciado laboratorio](./docs/Lab%201%20-%20MPI.pdf)
- **Soluciones**: 
    - [Solución Monolítica](./monolithic/)
    - [Solución Basado en servicios](./service_based/)
    - [Solución Basado en eventos](./event_driven/)

## Descripción

## Instrucciones

A continuación se detallan los pasos para ejecutar el programa, desde la instalación de las dependencias hasta la ejecución del programa de cada solución, para los requerimientos de cada solución esta la sección de [Versiones](#versiones).

### General
Las soluciones se encuentran en las carpetas `monolithic`, `service_based` y `event_driven`, cada una con su propio archivo `README.md` con las instrucciones para ejecutar el programa.

Para ejecutar la solución <folder_solution>(monolithic, service_based, event_driven) se deben seguir los siguientes pasos:

1. Instalar las dependencias necesarias:
```bash
pip install -r <folder_solution>/requirements.txt
```
o instalar las dependencias de forma manual abriendo el archivo `requirements.txt` y ejecutando el siguiente comando:
```bash
pip install <package>
```

2. Editar las variables de entorno en el archivo `.env` con los valores correspondientes (se debe acceder a la carpeta `monolithic`, `service_based` o `event_driven` para editar el archivo `.env`), en base a las credenciales para conectarse a la base de datos.
Siendo:
```env
DB_USER=<user>
DB_PASSWORD=<password>
DB_HOST=<host>
DB_PORT=<port>
DB_NAME=<database>
```

3. Ejecutar el programa:
```bash
python <folder_solution>/app.py
```
o
```bash
python3 <folder_solution>/app.py
```
o
```bash
py <folder_solution>/app.py
```
o para la solución basada en eventos:
```bash
mpiexec -n <number_of_processes> python <folder_solution>/app.py
```

3. Seguir las instrucciones del programa.

### General
Después de ejecutar el programa, se mostrará en terminal que se ha iniciado el servidor en el puerto 5000, para acceder a la interfaz gráfica se debe abrir un navegador y acceder a la dirección `http://localhost:5000/`.

En la interfaz se dispondra de tres botones, uno para cargar el archivo, otro para procesar el archivo y otro para descargar el archivo procesado. Los archivos se deben cargar en formato `.csv` y el archivo procesado se descargará en formato `.csv`. 
En caso de que se presione el botón 'Ver resultados' se mostrará en pantalla los resultados del procesamiento del archivo en forma json.
Tambien se dispone de un botón info que muestra información sobre el programa.

Otra forma de interactuar con el programa es mediante postman/hoppscotch, para ello se debe realizar un post a la dirección `http://localhost:5000/<request>` con un body de tipo form-data y una key llamada `file` con el archivo a procesar.
El flujo en postman/hoppscotch sería el siguiente:
1. Realizar un post a la dirección `http://localhost:5000/upload` con un body de tipo form-data y una key llamada `file` con el archivo a procesar.
2. Realizar un get a la dirección `http://localhost:5000/results` para ver los resultados del procesamiento del archivo.
3. Realizar un get a la dirección `http://localhost:5000/save` para descargar el archivo procesado.



## Versiones

A continuación se detallan las versiones de las herramientas utilizadas en cada solución.
- General
    - Python: 3.12.0
    - Pip: 24.0
    - PostgreSQL: 14.2+
    - HTML: 5
    - CSS: 3
    - JavaScript: 6

| Package         | Version       | Necesitas Instalarlo (No viene por defecto) |
|-----------------|---------------|--------------------------------------------|
| blinker         | 1.7.0         | No                                         |
| click           | 8.1.7         | No                                         |
| colorama        | 0.4.6         | No                                         |
| et-xmlfile      | 1.1.0         | No                                         |
| Flask           | 3.0.3         | Yes                                        |
| itsdangerous    | 2.2.0         | No                                         |
| Jinja2          | 3.1.3         | No                                         |
| MarkupSafe      | 2.1.5         | No                                         |
| mpi4py          | 3.1.6         | Yes                                        |
| numpy           | 1.26.4        | Yes                                        |
| pandas          | 2.2.2         | Yes                                        |
| pip             | 24.0.0        | No                                         |
| psycopg2-binary | 2.9.9         | Yes                                        |
| python-dateutil | 2.9.0.post0   | No                                         |
| pytz            | 2024.1        | No                                         |
| six             | 1.16.0        | No                                         |
| tzdata          | 2024.1        | No                                         |
| Werkzeug        | 3.0.2         | No                                         |
| psutil          | 5.9.8         | Yes                                        |
| python-dotenv   | 0.19.1        | Yes                                        |

- Servicios y Eventos:

Se necesita de instalar mpi en el sistema operativo, para ello se puede seguir el siguiente tutorial: [Instalación de MPI](https://learn.microsoft.com/en-us/message-passing-interface/microsoft-mpi), en otros sistemas operativos se puede seguir el siguiente tutorial: [Instalación de MPI en Linux](https://www.open-mpi.org/faq/?category=building#easy-build)

- Para el caso de la base de datos se necesita instalar PostgreSQL, para ello se puede seguir el siguiente tutorial: [Instalación de PostgreSQL](https://www.postgresql.org/download/), o tambien se puede instalar mediante docker, para ello se puede seguir el siguiente tutorial: [Instalación de PostgreSQL con Docker](https://hub.docker.com/_/postgres)

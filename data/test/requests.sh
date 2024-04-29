#!/bin/bash

# Número de peticiones concurrentes
CONCURRENCY_LEVELS=(15)

# URL del servicio
URL="http://localhost:5000/upload"

# Bucle sobre los diferentes niveles de concurrencia
for CONCURRENCY in "${CONCURRENCY_LEVELS[@]}"; do
    echo "Enviando $CONCURRENCY peticiones simultáneas..."
    
    # Genera el número necesario de comandos curl
    seq $CONCURRENCY | xargs -P $CONCURRENCY -I % curl --request POST \
        --url $URL \
        --header 'content-type: multipart/form-data' \
        --form file=@data_500.csv
    
    echo "Finalizado $CONCURRENCY peticiones simultáneas."
    echo "----------------"
done


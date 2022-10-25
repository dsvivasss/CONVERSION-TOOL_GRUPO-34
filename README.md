# Contenedor de Docker

## Docker image
Dentro del directorio api se encuentra una imagen Dockerfile que permite crear una imagen de Docker con la aplicación de Flask.

## Docker compose
En el directorio raiz del proyecto se encuentra un archivo docker-compose.yml que permite crear un contenedor de Docker con la aplicación de Flask y los servicios requeridos de Kafka.

   ```
   docker-compose -f docker-compose.yml up
   ```
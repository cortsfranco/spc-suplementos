#!/bin/bash

# Detener contenedores existentes
docker-compose down

# Construir nuevas imágenes
docker-compose build

# Ejecutar migraciones
docker-compose run web flask db upgrade

# Iniciar servicios
docker-compose up -d

# Verificar logs
docker-compose logs -f 
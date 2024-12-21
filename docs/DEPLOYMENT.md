# Guía de Despliegue

## Requisitos del Servidor

- Ubuntu 20.04 LTS
- 2GB RAM mínimo
- PostgreSQL 13+
- Redis 6+
- Nginx

## Pasos de Instalación

1. **Preparar Servidor** 
```
services:
  - type: web
    name: spc-suplementos
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn spc:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
      - key: FLASK_ENV
        value: production
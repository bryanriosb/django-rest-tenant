# README #

Estructura base para crear REST API con arquitectura multitenant, lo que permite crear plataformas de tipo SaaS con base de datos separada por Schemas

### Tecnología ###

* Django 4
* Channels
* Celery
* Celery Beat
* Redis
* Docker Compose
* Django Rest Framework
* PostgreSQL
* Django Tenants
* Django Rest Simple JWT


### ¿Qué características tiene el proyecto? ###

* Activación de cuenta por Email
* Recuperación de contraseña
* Gestión de Usuarios
* Configuración base para desarrollo y producción


### Levantar ###
En este ejemplo consideramos levantar el entorno de desarrollo

```
export COMPOSE_FILE=docker-compose.dev.yml
docker compose build
docker compose up -d
```


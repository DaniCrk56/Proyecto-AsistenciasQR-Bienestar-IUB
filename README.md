# 📌 Sistema de Gestión de Asistencias y Eventos - Bienestar IUB

Backend desarrollado con **FastAPI** y **PostgreSQL** para la gestión integral de actividades, inscripciones de usuarios mediante códigos QR y validación de asistencias, implementando estrictos estándares de arquitectura limpia y seguridad de datos.

---

## 🚀 Tecnologías y Herramientas

* **Framework:** FastAPI (Python)
* **Servidor ASGI:** Uvicorn
* **Base de Datos:** PostgreSQL (Neon DB)
* **Conexión SQL:** `psycopg2` con consultas parametrizadas anti-inyección SQL.

---

## 🏛️ Arquitectura del Proyecto

El proyecto está estructurado bajo el **Patrón Repositorio** y el principio de **Separación de Responsabilidades (SoC)**:

```text
app/
├── core/             # Configuración centralizada de base de datos
├── models/           # Definición de entidades / modelos de dominio
└── repositories/     # Capa de acceso a datos (CRUDs independientes por tabla)

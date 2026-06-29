# Sistema de Gestión de Biblioteca Digital

Trabajo Práctico Final – Unidad I  
Programación Avanzada – Licenciatura en Ciencia de Datos - UNAB

---

## Descripción

Sistema desarrollado en Python que permite administrar libros, usuarios y préstamos de una biblioteca digital, aplicando Programación Orientada a Objetos.

El sistema permite:
- Dar de alta, modificar, dar de baja y listar libros y usuarios
- Registrar préstamos y devoluciones
- Consultar préstamos activos
- Validar que un libro no pueda prestarse si ya tiene un préstamo activo

---

## Integrantes

- Marcos Ruiz Diaz 44052687
- Leandro Rodriguez 42902020

---

## Tecnologías

- Python 3
- Módulo `datetime` (biblioteca estándar)

---

## Estructura del proyecto

| Archivo | Descripción |
|---|---|
| `main.py` | Código fuente principal del sistema |
| `Diagrama de flujo` | Diagrama de flujo |
| `README.md` | Este archivo |

---

## Clases principales

- **`persona`** — clase base con nombre, apellido y DNI
- **`Usuario`** — hereda de `persona`, agrega correo electrónico
- **`Libro`** — representa un libro con sus datos y estado de préstamo
- **`Prestamo`** — registra la relación entre un libro y un usuario, con fechas
- **`Biblioteca`** — clase central que gestiona todas las operaciones

---

## Decisiones de diseño

- **Patrón Singleton** (`SingletonMeta`): garantiza que exista una única instancia de `Biblioteca`, evitando datos inconsistentes.
- **Decorador `log_operacion`**: registra en consola cada operación importante del sistema.
- **Herencia**: `Usuario` extiende `persona`.
- **Polimorfismo**: `mostrar_info()` está implementado de forma distinta en cada clase.
- **Composición**: `Prestamo` es creado y gestionado exclusivamente por `Biblioteca`.
- **Agregación**: `Libro` y `Usuario` existen independientemente de `Biblioteca`.
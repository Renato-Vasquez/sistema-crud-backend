# 📦 API Sistema de Gestión

API REST desarrollada con Flask y MySQL para la gestión de usuarios, tareas, productos y categorías.

---

## 🚀 Tecnologías utilizadas

- Python
- Flask
- MySQL
- Flask-MySQLdb
- Werkzeug (hash de contraseñas)
- Thunder Client (para pruebas)

---

## 📁 Estructura del proyecto
API_sistema_gestion/
│
├── src/
│ ├── app.py
│ ├── config.py
│ ├── extensions.py
│ └── routes/
│ ├── usuarios.py
│ ├── tareas.py
│ ├── productos.py
│ └── categorias.py
│
├── requirements.txt
└── README.md

## 🧱 Funcionalidades

### 👤 Usuarios
- Crear usuario
- Listar usuarios
- Obtener usuario por ID
- Actualizar usuario
- Eliminar usuario
- Contraseñas encriptadas con hash seguro

### 📝 Tareas
- CRUD completo
- Relación con usuarios
- Eliminación en cascada (ON DELETE CASCADE)

### 🏷 Categorías
- CRUD completo

### 📦 Productos
- CRUD completo
- Validación de categoría existente
- Relación con categorías

---

## 🔗 Endpoints principales

### Usuarios
- GET `/usuarios/`
- GET `/usuarios/<id>`
- POST `/usuarios/`
- PUT `/usuarios/<id>`
- DELETE `/usuarios/<id>`

### Tareas
- GET `/tareas/`
- POST `/tareas/`
- PUT `/tareas/<id>`
- DELETE `/tareas/<id>`

### Categorías
- GET `/categorias/`
- POST `/categorias/`


### Productos
- GET `/productos/`
- POST `/productos/`
- PUT `/productos/<id>`
- DELETE `/productos/<id>`



## 🛠 Instalación y ejecución

1. Clonar el repositorio:


git clone https://github.com/Renato-Vasquez/sistema-crud-backend.git


2. Crear entorno virtual:
python -m venv env


3. Activar entorno virtual:
env\Scripts\activate

4. Instalar dependencias:
pip install -r requirements.txt


5. Configurar base de datos en `config.py`

6. Ejecutar el servidor:
python src/app.py


---

## 🎯 Objetivo del proyecto

Desarrollar un sistema backend modular con arquitectura REST, base de datos relacional y buenas prácticas básicas de seguridad para fortalecer conocimientos en desarrollo backend con Python.

---

## 👨‍💻 Autor

Proyecto desarrollado como práctica para fortalecimiento de habilidades backend.
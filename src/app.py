from flask import Flask
from config import config
from extensions import mysql

# Importar Blueprints
from routes.usuarios import usuarios_bp
from routes.productos import productos_bp
from routes.categorias import categorias_bp
from routes.tareas import tareas_bp

app = Flask(__name__)
app.config.from_object(config['development'])

# Inicializar MySQL
mysql.init_app(app)

# Registrar Blueprints
app.register_blueprint(usuarios_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(tareas_bp)

if __name__ == '__main__':
    app.run()
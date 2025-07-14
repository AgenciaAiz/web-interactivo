import os
import sys

# La línea sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
# es generalmente innecesaria en entornos de despliegue como Render
# si tu estructura de carpetas es estándar y los imports son relativos.
# La dejaremos comentada por ahora para evitar posibles conflictos.
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db # Asegúrate de que src/models/__init__.py exista
from src.routes.user import user_bp # Asegúrate de que src/routes/__init__.py exista
from src.routes.chatbot import chatbot_bp # Asegúrate de que src/routes/__init__.py exista

# Inicializa la aplicación Flask
# El nombre de la variable 'app' es importante para Gunicorn (gunicorn run_server:app)
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'src', 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilita CORS para todas las rutas
CORS(app)

# Registra los Blueprints para las rutas de usuario y chatbot
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(chatbot_bp, url_prefix='/api')

# --- Configuración de la Base de Datos SQLite ---
# En Render, el sistema de archivos es efímero.
# Si necesitas persistencia de datos, deberías usar una base de datos externa
# como PostgreSQL (Render ofrece una capa gratuita).
# Para que SQLite funcione temporalmente, debe estar en /tmp.
# Sin embargo, si no necesitas la base de datos activa para el despliegue inicial,
# es mejor mantenerla comentada o usar una base de datos externa.
# Si la activas, asegúrate de que la ruta sea a /tmp para que sea escribible.
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join('/tmp', 'app.db')}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
# with app.app_context():
#     db.create_all()
# --- FIN Configuración de la Base de Datos ---

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder

    # Verifica si la carpeta estática no está configurada
    if static_folder_path is None:
        return "Static folder not configured", 404 # Agregado el return

    # Si la ruta no está vacía y el archivo existe en la carpeta estática, sírvelo
    # Asegúrate de que el path.exists esté completo
    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path) # Agregado el return
    else:
        # Si la ruta está vacía o el archivo no existe, intenta servir index.html
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            # Si index.html no se encuentra, devuelve un 404
            return "index.html not found", 404 # Agregado el return y mensaje

# Esta parte solo se ejecuta cuando corres el script directamente (ej. python run_server.py)
# No se ejecuta cuando Gunicorn inicia la aplicación en Render.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

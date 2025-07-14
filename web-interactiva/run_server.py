import os
import sys # Asegúrate de que sys esté importado
raise Exception("DEBUG: Reached top of run_server.py - FORCED ERROR")
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.chatbot import chatbot_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'src', 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
print(f"DEBUG: Flask app initialized. Static folder: {app.static_folder}", file=sys.stderr)


CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(chatbot_bp, url_prefix='/api')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    print(f"DEBUG: Serve function called for path: {path}", file=sys.stderr)
    static_folder_path = app.static_folder
    print(f"DEBUG: Static folder path inside serve: {static_folder_path}", file=sys.stderr)
    
    if static_folder_path is None:
        print("DEBUG: Static folder not configured (is None)", file=sys.stderr) # Para más detalle
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        print(f"DEBUG: Serving specific file: {path}", file=sys.stderr) # Para más detalle
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        print(f"DEBUG: Checking for index.html at: {index_path}", file=sys.stderr) # Para más detalle
        if os.path.exists(index_path):
            print("DEBUG: Serving index.html", file=sys.stderr) # Para más detalle
            return send_from_directory(static_folder_path, 'index.html')
        else:
            print("DEBUG: index.html not found at expected path", file=sys.stderr) # Para más detalle
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

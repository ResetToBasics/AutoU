"""
Aplicação Flask principal para classificação de emails
"""
import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS

# Adicionar diretório raiz ao path para imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from backend.config import config
from backend.routes.email_routes import email_bp


def create_app(config_name=None):
    """
    Factory function para criar a aplicação Flask
    """
    app = Flask(__name__, 
                static_folder='../frontend',
                template_folder='../frontend')
    
    # Carregar configuração
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Habilitar CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Registrar blueprints (importante: antes das rotas estáticas)
    app.register_blueprint(email_bp, url_prefix='/api')
    
    # Rota de health check
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'message': 'Email Classification API is running'}, 200
    
    # Rotas para servir arquivos estáticos do frontend
    @app.route('/css/<path:filename>')
    def serve_css(filename):
        css_path = os.path.join(app.static_folder, 'css')
        return send_from_directory(css_path, filename)
    
    @app.route('/js/<path:filename>')
    def serve_js(filename):
        js_path = os.path.join(app.static_folder, 'js')
        return send_from_directory(js_path, filename)
    
    # Rota para servir a interface web (deve ser a última)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        # Se não for uma rota da API, servir o frontend
        if not path.startswith('api'):
            if path and os.path.exists(os.path.join(app.static_folder, path)):
                return send_from_directory(app.static_folder, path)
            return send_from_directory(app.static_folder, 'index.html')
        return {'error': 'Not found'}, 404
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )


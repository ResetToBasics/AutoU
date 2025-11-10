"""
Script de inicialização da aplicação
Execute este arquivo para iniciar o servidor Flask
"""
import os
import sys

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app

if __name__ == '__main__':
    app = create_app()
    # Suporta PORT (Heroku/Render) ou FLASK_PORT
    port = int(os.environ.get('PORT', app.config['PORT']))
    app.run(
        host=app.config['HOST'],
        port=port,
        debug=app.config['DEBUG']
    )


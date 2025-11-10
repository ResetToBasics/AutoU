"""
Configurações da aplicação Flask
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuração base da aplicação"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    # Suporta PORT (Heroku/Render) ou FLASK_PORT
    PORT = int(os.environ.get('PORT', os.environ.get('FLASK_PORT', 5000)))
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf'}
    
    @staticmethod
    def init_app(app):
        """Inicializa configurações adicionais da aplicação"""
        # Criar diretório de uploads se não existir
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)


class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True


class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False


class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


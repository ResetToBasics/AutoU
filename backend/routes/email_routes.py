"""
Rotas da API para classificação de emails
"""
import os
import sys
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

# Garantir que o path está configurado
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.processors.text_processor import TextProcessor
from src.processors.pdf_processor import PDFProcessor
from src.classifiers.email_classifier import EmailClassifier
from src.generators.response_generator import ResponseGenerator

email_bp = Blueprint('email', __name__)

# Variáveis globais para processadores (serão inicializados na primeira requisição)
text_processor = None
pdf_processor = None
email_classifier = None
response_generator = None


def get_processors():
    """Inicializa e retorna os processadores (lazy loading)"""
    global text_processor, pdf_processor, email_classifier, response_generator
    
    if text_processor is None:
        text_processor = TextProcessor()
    if pdf_processor is None:
        pdf_processor = PDFProcessor()
    if email_classifier is None:
        email_classifier = EmailClassifier()
    if response_generator is None:
        response_generator = ResponseGenerator()
    
    return text_processor, pdf_processor, email_classifier, response_generator


def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf'}


@email_bp.route('/classify', methods=['POST'])
def classify_email():
    """
    Endpoint para classificar email e gerar resposta automática
    
    Aceita:
    - text: texto direto do email
    - file: arquivo .txt ou .pdf
    """
    try:
        # Inicializar processadores
        text_proc, pdf_proc, email_class, response_gen = get_processors()
        
        # Verificar se há texto direto
        if request.is_json and 'text' in request.json and request.json['text']:
            email_text = request.json['text']
        # Verificar se há arquivo enviado
        elif 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({'error': 'Tipo de arquivo não permitido. Use .txt ou .pdf'}), 400
            
            # Processar arquivo
            filename = secure_filename(file.filename)
            file_extension = filename.rsplit('.', 1)[1].lower()
            
            if file_extension == 'txt':
                email_text = text_proc.process_file(file)
            elif file_extension == 'pdf':
                email_text = pdf_proc.process_file(file)
            else:
                return jsonify({'error': 'Formato de arquivo não suportado'}), 400
        else:
            return jsonify({'error': 'Envie um texto ou arquivo para classificação'}), 400
        
        # Validar que o texto não está vazio
        if not email_text or len(email_text.strip()) == 0:
            return jsonify({'error': 'Texto do email está vazio'}), 400
        
        # Classificar email
        classification_result = email_class.classify(email_text)
        
        # Gerar resposta automática
        response_text = response_gen.generate_response(
            email_text, 
            classification_result['category']
        )
        
        # Retornar resultado
        return jsonify({
            'category': classification_result['category'],
            'confidence': classification_result['confidence'],
            'suggested_response': response_text,
            'processed_text_length': len(email_text)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao processar email',
            'message': str(e)
        }), 500


@email_bp.route('/classify/text', methods=['POST'])
def classify_text():
    """
    Endpoint simplificado para classificar apenas texto
    """
    try:
        # Inicializar processadores
        _, _, email_class, response_gen = get_processors()
        
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Campo "text" é obrigatório'}), 400
        
        email_text = data['text']
        if not email_text or len(email_text.strip()) == 0:
            return jsonify({'error': 'Texto do email está vazio'}), 400
        
        # Classificar email
        classification_result = email_class.classify(email_text)
        
        # Gerar resposta automática
        response_text = response_gen.generate_response(
            email_text, 
            classification_result['category']
        )
        
        return jsonify({
            'category': classification_result['category'],
            'confidence': classification_result['confidence'],
            'suggested_response': response_text
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao processar email',
            'message': str(e)
        }), 500


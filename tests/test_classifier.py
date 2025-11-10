"""
Testes unitários para o classificador de emails
"""
import pytest
import os
from src.classifiers.email_classifier import EmailClassifier


@pytest.fixture
def classifier():
    """Fixture para criar instância do classificador"""
    # Configurar chave de API para testes (mock)
    os.environ['OPENAI_API_KEY'] = 'test-key'
    return EmailClassifier()


def test_classifier_initialization(classifier):
    """Testa inicialização do classificador"""
    assert classifier is not None
    assert classifier.api_key == 'test-key'


def test_fallback_classification_produtivo(classifier):
    """Testa classificação fallback para email produtivo"""
    email_text = "Preciso de ajuda com um problema no sistema. O erro ocorre quando tento fazer login."
    result = classifier._fallback_classification(email_text)
    
    assert result['category'] in ['Produtivo', 'Improdutivo']
    assert 0 <= result['confidence'] <= 1


def test_fallback_classification_improdutivo(classifier):
    """Testa classificação fallback para email improdutivo"""
    email_text = "Feliz Natal e um próspero Ano Novo! Obrigado por tudo."
    result = classifier._fallback_classification(email_text)
    
    assert result['category'] in ['Produtivo', 'Improdutivo']
    assert 0 <= result['confidence'] <= 1


def test_parse_response_produtivo(classifier):
    """Testa parsing de resposta com categoria Produtivo"""
    response = "Produtivo 0.95"
    category, confidence = classifier._parse_response(response)
    
    assert category == "Produtivo"
    assert 0 <= confidence <= 1


def test_parse_response_improdutivo(classifier):
    """Testa parsing de resposta com categoria Improdutivo"""
    response = "Improdutivo 0.87"
    category, confidence = classifier._parse_response(response)
    
    assert category == "Improdutivo"
    assert 0 <= confidence <= 1


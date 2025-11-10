"""
Classificador de emails usando OpenAI API quando disponível
"""
import os
import re
from typing import Any, Dict, Tuple

try:
    import openai as openai_module
except ImportError:
    openai_module = None  # type: ignore

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore


class EmailClassifier:
    """Classe para classificar emails em Produtivo ou Improdutivo"""
    
    def __init__(self):
        """Inicializa o classificador"""
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.model = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
        self._client = None
        self._legacy_client = None
        
        if self.api_key:
            if openai_module and hasattr(openai_module, "ChatCompletion"):
                openai_module.api_key = self.api_key
                self._legacy_client = openai_module
            elif OpenAI is not None:
                self._client = OpenAI(api_key=self.api_key)
            else:
                # Client indisponível nesta versão da SDK
                self.api_key = None
        
        # Prompts para classificação
        self.classification_prompt = """Você é um assistente especializado em classificar emails corporativos.

Classifique o seguinte email em uma das duas categorias:

1. **Produtivo**: Emails que requerem uma ação ou resposta específica
   - Solicitações de suporte técnico
   - Atualização sobre casos em aberto
   - Dúvidas sobre o sistema
   - Pedidos de informações
   - Solicitações de alterações
   - Problemas que precisam ser resolvidos

2. **Improdutivo**: Emails que não necessitam de uma ação imediata
   - Mensagens de felicitações (aniversário, natal, ano novo, etc.)
   - Agradecimentos genéricos
   - Mensagens informativas sem ação necessária
   - Spam ou conteúdo irrelevante

Responda APENAS com uma das duas palavras: "Produtivo" ou "Improdutivo", seguido de um número entre 0 e 1 representando a confiança da classificação (ex: "Produtivo 0.95").

Email para classificar:
"""
    
    def classify(self, email_text: str) -> Dict[str, Any]:
        """
        Classifica um email em Produtivo ou Improdutivo
        
        Args:
            email_text: Texto do email a ser classificado
            
        Returns:
            dict: Dicionário com categoria e confiança
                {
                    'category': 'Produtivo' ou 'Improdutivo',
                    'confidence': float (0-1)
                }
        """
        # Usar heurística caso não haja chave ou cliente configurado
        if not self.api_key or (self._client is None and self._legacy_client is None):
            return self._fallback_classification(email_text)
        
        try:
            # Preparar prompt
            full_prompt = self.classification_prompt + email_text
            
            # Chamar API da OpenAI
            response = self._invoke_openai(full_prompt)
            
            # Extrair resposta
            result = response.strip()
            
            # Processar resposta
            category, confidence = self._parse_response(result)
            
            return {
                'category': category,
                'confidence': confidence
            }
            
        except Exception:
            # Em caso de erro, usar fallback por palavras-chave
            return self._fallback_classification(email_text)
    
    def _invoke_openai(self, prompt: str) -> str:
        """
        Invoca a API da OpenAI usando o client disponível
        """
        messages = [
            {"role": "system", "content": "Você é um classificador de emails profissional e preciso."},
            {"role": "user", "content": prompt}
        ]
        
        if self._client:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=50
            )
            return response.choices[0].message.content.strip()
        
        if self._legacy_client:
            response = self._legacy_client.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=50
            )
            message = response.choices[0].message
            if isinstance(message, dict):
                return message.get('content', '').strip()
            return message.content.strip()
        
        raise RuntimeError("Cliente OpenAI não configurado.")
    
    def _parse_response(self, response: str) -> Tuple[str, float]:
        """
        Parse da resposta da API
        
        Args:
            response: Resposta da API
            
        Returns:
            tuple: (categoria, confiança)
        """
        response = response.strip()
        
        response_lower = response.lower()
        
        # Verificar se contém os termos das categorias (ordem importa para evitar falso positivo)
        if "improdutivo" in response_lower:
            category = "Improdutivo"
        elif "produtivo" in response_lower:
            category = "Produtivo"
        else:
            # Tentar classificação por palavras-chave como fallback
            category = "Produtivo"  # Default
        
        # Extrair confiança (número entre 0 e 1)
        confidence_match = re.search(r'(\d+\.?\d*)', response)
        if confidence_match:
            try:
                confidence = float(confidence_match.group(1))
                # Normalizar para 0-1
                if confidence > 1:
                    confidence = confidence / 100
                confidence = max(0.0, min(1.0, confidence))
            except:
                confidence = 0.8
        else:
            confidence = 0.8
        
        return category, confidence
    
    def _fallback_classification(self, email_text: str) -> Dict[str, Any]:
        """
        Classificação básica por palavras-chave quando a API falha
        
        Args:
            email_text: Texto do email
            
        Returns:
            dict: Dicionário com categoria e confiança
        """
        email_lower = email_text.lower()
        
        # Palavras-chave para emails produtivos
        productive_keywords = [
            'solicito', 'preciso', 'problema', 'erro', 'bug', 'ajuda',
            'suporte', 'dúvida', 'questão', 'atualização', 'status',
            'pedido', 'requisição', 'alteração', 'correção', 'urgente',
            'request', 'issue', 'problem', 'help', 'support', 'update',
            'question', 'change', 'fix', 'urgent'
        ]
        
        # Palavras-chave para emails improdutivos
        unproductive_keywords = [
            'feliz natal', 'feliz ano novo', 'parabéns', 'congratulações',
            'obrigado', 'thanks', 'thank you', 'agradeço', 'agradecimento',
            'felicitações', 'aniversário', 'birthday', 'congratulations',
            'boas festas', 'happy new year', 'merry christmas'
        ]
        
        # Contar ocorrências
        productive_count = sum(1 for keyword in productive_keywords if keyword in email_lower)
        unproductive_count = sum(1 for keyword in unproductive_keywords if keyword in email_lower)
        
        # Classificar
        if unproductive_count > productive_count:
            category = "Improdutivo"
            confidence = min(0.9, 0.6 + (unproductive_count * 0.1))
        else:
            category = "Produtivo"
            confidence = min(0.9, 0.6 + (productive_count * 0.1))
        
        return {
            'category': category,
            'confidence': confidence
        }

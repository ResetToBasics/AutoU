"""
Gerador de respostas automáticas usando OpenAI API (com fallback local)
"""
import os

try:
    import openai as openai_module
except ImportError:
    openai_module = None  # type: ignore

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore


class ResponseGenerator:
    """Classe para gerar respostas automáticas baseadas na classificação do email"""
    
    def __init__(self):
        """Inicializa o gerador de respostas"""
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
                self.api_key = None
        
        # Templates de prompt por categoria
        self.productive_prompt = """Você é um assistente profissional de uma empresa do setor financeiro.

Um cliente enviou o seguinte email que foi classificado como **Produtivo** (requer ação ou resposta):

"{email_text}"

Gere uma resposta profissional, cortês e adequada para este email. A resposta deve:
- Ser profissional e respeitosa
- Responder ou abordar as questões levantadas
- Ser concisa mas completa
- Manter o tom corporativo apropriado
- Se for uma solicitação, indicar que a equipe está trabalhando na questão
- Se for uma dúvida, fornecer informações úteis ou indicar que será respondida em breve

Gere APENAS o texto da resposta, sem saudações adicionais ou explicações."""
        
        self.unproductive_prompt = """Você é um assistente profissional de uma empresa do setor financeiro.

Um cliente enviou o seguinte email que foi classificado como **Improdutivo** (não requer ação imediata):

"{email_text}"

Gere uma resposta breve, profissional e cortês para este email. A resposta deve:
- Ser profissional e respeitosa
- Agradecer ou reconhecer a mensagem
- Ser concisa
- Manter o tom corporativo apropriado
- Não ser excessivamente longa, já que é uma mensagem que não requer ação

Gere APENAS o texto da resposta, sem saudações adicionais ou explicações."""
    
    def generate_response(self, email_text: str, category: str) -> str:
        """
        Gera uma resposta automática baseada no email e na categoria
        
        Args:
            email_text: Texto do email original
            category: Categoria do email ('Produtivo' ou 'Improdutivo')
            
        Returns:
            str: Resposta automática gerada
        """
        if not self.api_key or (self._client is None and self._legacy_client is None):
            return self._generate_fallback_response(category)
        
        try:
            # Selecionar prompt baseado na categoria
            if category.lower() == "produtivo":
                prompt = self.productive_prompt.format(email_text=email_text)
            else:
                prompt = self.unproductive_prompt.format(email_text=email_text)
            
            # Chamar API da OpenAI
            generated_response = self._invoke_openai(prompt)
            return generated_response
            
        except Exception:
            # Em caso de erro, retornar resposta genérica
            return self._generate_fallback_response(category)
    
    def _invoke_openai(self, prompt: str) -> str:
        """
        Invoca a API utilizando o client disponível
        """
        messages = [
            {"role": "system", "content": "Você é um assistente profissional de uma empresa do setor financeiro, especializado em gerar respostas automáticas para emails."},
            {"role": "user", "content": prompt}
        ]
        
        if self._client:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        
        if self._legacy_client:
            response = self._legacy_client.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            message = response.choices[0].message
            if isinstance(message, dict):
                return message.get('content', '').strip()
            return message.content.strip()
        
        raise RuntimeError("Cliente OpenAI não configurado.")
    
    def _generate_fallback_response(self, category: str) -> str:
        """
        Gera uma resposta genérica quando a API falha
        
        Args:
            category: Categoria do email
            
        Returns:
            str: Resposta genérica
        """
        if category.lower() == "produtivo":
            return """Prezado(a),

Agradecemos seu contato. Nossa equipe analisará sua solicitação e retornará em breve.

Atenciosamente,
Equipe de Atendimento"""
        else:
            return """Prezado(a),

Agradecemos sua mensagem.

Atenciosamente,
Equipe de Atendimento"""

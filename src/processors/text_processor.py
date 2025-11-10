"""
Processador de texto para emails
"""
import re
import string


class TextProcessor:
    """Classe para processar e limpar textos de emails"""
    
    def __init__(self):
        """Inicializa o processador de texto"""
        self.stop_words = {
            'a', 'o', 'e', 'de', 'do', 'da', 'em', 'um', 'uma', 'para',
            'com', 'não', 'que', 'é', 'como', 'mas', 'se', 'ou', 'mais',
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
            'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
            'do', 'at', 'this', 'but', 'his', 'by', 'from'
        }
    
    def process_file(self, file):
        """
        Processa um arquivo de texto e retorna o conteúdo
        
        Args:
            file: Arquivo de texto (.txt)
            
        Returns:
            str: Conteúdo do arquivo processado
        """
        try:
            content = file.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            return self.clean_text(content)
        except Exception as e:
            raise Exception(f"Erro ao processar arquivo de texto: {str(e)}")
    
    def clean_text(self, text):
        """
        Limpa e normaliza o texto
        
        Args:
            text: Texto a ser limpo
            
        Returns:
            str: Texto limpo
        """
        if not text:
            return ""
        
        # Converter para minúsculas
        text = text.lower()
        
        # Remover URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remover emails
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remover caracteres especiais, mas manter pontuação básica
        text = re.sub(r'[^\w\s\.\?\!\,]', ' ', text)
        
        # Remover múltiplos espaços
        text = re.sub(r'\s+', ' ', text)
        
        # Remover espaços no início e fim
        text = text.strip()
        
        return text
    
    def remove_stop_words(self, text):
        """
        Remove stop words do texto
        
        Args:
            text: Texto para remover stop words
            
        Returns:
            str: Texto sem stop words
        """
        words = text.split()
        filtered_words = [word for word in words if word not in self.stop_words]
        return ' '.join(filtered_words)
    
    def extract_keywords(self, text, max_keywords=10):
        """
        Extrai palavras-chave do texto
        
        Args:
            text: Texto para extrair keywords
            max_keywords: Número máximo de keywords
            
        Returns:
            list: Lista de palavras-chave
        """
        text = self.clean_text(text)
        text = self.remove_stop_words(text)
        words = text.split()
        
        # Contar frequência de palavras
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Apenas palavras com mais de 3 caracteres
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Ordenar por frequência
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Retornar top keywords
        return [word for word, freq in sorted_words[:max_keywords]]


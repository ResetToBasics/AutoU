"""
Processador de PDF para extrair texto de emails em formato PDF
"""
import PyPDF2
import io


class PDFProcessor:
    """Classe para processar arquivos PDF e extrair texto"""
    
    def __init__(self):
        """Inicializa o processador de PDF"""
        pass
    
    def process_file(self, file):
        """
        Processa um arquivo PDF e retorna o texto extraído
        
        Args:
            file: Arquivo PDF
            
        Returns:
            str: Texto extraído do PDF
        """
        try:
            # Ler conteúdo do arquivo
            file_content = file.read()
            
            # Criar objeto PDF reader
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            
            # Extrair texto de todas as páginas
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            if not text or len(text.strip()) == 0:
                raise Exception("Não foi possível extrair texto do PDF. O arquivo pode estar corrompido ou ser uma imagem.")
            
            return text.strip()
            
        except PyPDF2.errors.PdfReadError as e:
            raise Exception(f"Erro ao ler PDF: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao processar arquivo PDF: {str(e)}")


// Configuração da API
const API_BASE_URL = window.location.origin;
const API_ENDPOINT = `${API_BASE_URL}/api/classify`;

// Elementos do DOM
const textTab = document.getElementById('text-tab');
const fileTab = document.getElementById('file-tab');
const tabButtons = document.querySelectorAll('.tab-button');
const emailTextarea = document.getElementById('email-text');
const fileInput = document.getElementById('file-input');
const fileName = document.getElementById('file-name');
const classifyButton = document.getElementById('classify-button');
const buttonLoader = document.getElementById('button-loader');
const resultsSection = document.getElementById('results-section');
const errorSection = document.getElementById('error-section');
const errorMessage = document.getElementById('error-message');
const categoryValue = document.getElementById('category-value');
const confidenceBadge = document.getElementById('confidence-badge');
const confidenceFill = document.getElementById('confidence-fill');
const confidencePercentage = document.getElementById('confidence-percentage');
const responseText = document.getElementById('response-text');
const copyButton = document.getElementById('copy-button');

// Gerenciamento de Tabs
tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.getAttribute('data-tab');
        
        // Atualizar botões
        tabButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        
        // Atualizar conteúdo
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        if (tabName === 'text') {
            textTab.classList.add('active');
        } else {
            fileTab.classList.add('active');
        }
        
        // Limpar resultados
        hideResults();
        hideError();
    });
});

// Gerenciamento de Upload de Arquivo
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        fileName.textContent = `Arquivo selecionado: ${file.name}`;
        fileName.classList.add('show');
    } else {
        fileName.classList.remove('show');
    }
});

// Drag and Drop
const fileLabel = document.querySelector('.file-label');
const fileUploadWrapper = document.querySelector('.file-upload-wrapper');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    fileLabel.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    fileLabel.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    fileLabel.addEventListener(eventName, unhighlight, false);
});

function highlight() {
    fileLabel.style.borderColor = 'var(--primary-color)';
    fileLabel.style.background = 'rgba(37, 99, 235, 0.1)';
}

function unhighlight() {
    fileLabel.style.borderColor = 'var(--border-color)';
    fileLabel.style.background = 'var(--background-color)';
}

fileLabel.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        fileInput.files = files;
        fileName.textContent = `Arquivo selecionado: ${files[0].name}`;
        fileName.classList.add('show');
    }
}

// Função de Classificação
classifyButton.addEventListener('click', async () => {
    hideResults();
    hideError();
    
    // Verificar qual tab está ativa
    const activeTab = document.querySelector('.tab-button.active').getAttribute('data-tab');
    
    let formData = new FormData();
    let hasContent = false;
    
    if (activeTab === 'text') {
        const text = emailTextarea.value.trim();
        if (!text) {
            showError('Por favor, insira o texto do email antes de classificar.');
            return;
        }
        hasContent = true;
    } else {
        const file = fileInput.files[0];
        if (!file) {
            showError('Por favor, selecione um arquivo antes de classificar.');
            return;
        }
        formData.append('file', file);
        hasContent = true;
    }
    
    if (!hasContent) {
        showError('Por favor, forneça um texto ou arquivo para classificação.');
        return;
    }
    
    // Mostrar loading
    setLoading(true);
    
    try {
        let response;
        
        if (activeTab === 'text') {
            // Enviar como JSON
            response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: emailTextarea.value.trim()
                })
            });
        } else {
            // Enviar como FormData
            response = await fetch(API_ENDPOINT, {
                method: 'POST',
                body: formData
            });
        }
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Erro ao processar email');
        }
        
        // Mostrar resultados
        showResults(data);
        
    } catch (error) {
        console.error('Erro:', error);
        showError(error.message || 'Erro ao classificar email. Verifique sua conexão e tente novamente.');
    } finally {
        setLoading(false);
    }
});

// Função para mostrar resultados
function showResults(data) {
    const { category, confidence, suggested_response } = data;
    
    // Atualizar categoria
    categoryValue.textContent = category;
    categoryValue.className = `category-value ${category.toLowerCase()}`;
    
    // Atualizar confiança
    const confidencePercent = Math.round(confidence * 100);
    confidenceBadge.textContent = `${confidencePercent}%`;
    confidenceFill.style.width = `${confidencePercent}%`;
    confidencePercentage.textContent = `${confidencePercent}%`;
    
    // Atualizar resposta
    responseText.textContent = suggested_response;
    
    // Mostrar seção de resultados
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Função para esconder resultados
function hideResults() {
    resultsSection.style.display = 'none';
}

// Função para mostrar erro
function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Função para esconder erro
function hideError() {
    errorSection.style.display = 'none';
}

// Função para controlar loading
function setLoading(loading) {
    if (loading) {
        classifyButton.disabled = true;
        buttonLoader.classList.add('show');
        classifyButton.querySelector('.button-text').textContent = 'Processando...';
    } else {
        classifyButton.disabled = false;
        buttonLoader.classList.remove('show');
        classifyButton.querySelector('.button-text').textContent = 'Classificar Email';
    }
}

// Função para copiar resposta
copyButton.addEventListener('click', () => {
    const text = responseText.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        const originalText = copyButton.textContent;
        copyButton.textContent = 'Copiado!';
        copyButton.style.background = 'var(--success-color)';
        copyButton.style.borderColor = 'var(--success-color)';
        copyButton.style.color = 'white';
        
        setTimeout(() => {
            copyButton.textContent = originalText;
            copyButton.style.background = '';
            copyButton.style.borderColor = '';
            copyButton.style.color = '';
        }, 2000);
    }).catch(err => {
        console.error('Erro ao copiar:', err);
        showError('Erro ao copiar resposta para a área de transferência.');
    });
});

// Permitir Enter para enviar (apenas na textarea, não submit do form)
emailTextarea.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        classifyButton.click();
    }
});

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    console.log('Sistema de Classificação de Emails carregado');
});


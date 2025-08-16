// Configuração da API
const API_BASE_URL = '/api';

// Estado da aplicação
let produtoAtual = null;

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupTabNavigation();
    setupEventListeners();
    loadInitialData();
}

// Navegação por abas
function setupTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
            
            // Load data for the active tab
            loadTabData(targetTab);
        });
    });
}

// Event listeners
function setupEventListeners() {
    // Formulário de produto
    document.getElementById('form-produto').addEventListener('submit', handleProdutoSubmit);
    
    // Busca de produto
    document.getElementById('btn-buscar').addEventListener('click', handleBuscarProduto);
    document.getElementById('busca-codigo').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleBuscarProduto();
        }
    });
    
    // Formulário de contagem
    document.getElementById('form-contagem').addEventListener('submit', handleContagemSubmit);
    
    // Relatórios
    document.getElementById('btn-relatorio-pdf').addEventListener('click', () => gerarRelatorio('pdf'));
    document.getElementById('btn-relatorio-excel').addEventListener('click', () => gerarRelatorio('excel'));
    document.getElementById('btn-atualizar-resumo').addEventListener('click', carregarResumo);
    
    // Importação
    document.getElementById('btn-baixar-template').addEventListener('click', baixarTemplate);
    document.getElementById('btn-importar-excel').addEventListener('click', importarExcel);
    
    // Modal
    document.querySelector('.close').addEventListener('click', closeModal);
    document.getElementById('modal').addEventListener('click', function(e) {
        if (e.target === this) {
            closeModal();
        }
    });
}

// Carregamento inicial de dados
function loadInitialData() {
    carregarProdutos();
    carregarContagens();
    carregarResumo();
}

// Carregamento de dados por aba
function loadTabData(tab) {
    switch(tab) {
        case 'produtos':
            carregarProdutos();
            break;
        case 'contagem':
            carregarContagens();
            break;
        case 'relatorios':
            carregarResumo();
            break;
    }
}

// Funções de produto
async function handleProdutoSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const produtoData = {
        codigo: formData.get('codigo').trim(),
        nome: formData.get('nome').trim()
    };
    
    if (!produtoData.codigo || !produtoData.nome) {
        showMessage('Erro', 'Código e nome são obrigatórios', 'error');
        return;
    }
    
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/produtos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(produtoData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage('Sucesso', 'Produto cadastrado com sucesso!', 'success');
            e.target.reset();
            carregarProdutos();
        } else {
            showMessage('Erro', result.erro || 'Erro ao cadastrar produto', 'error');
        }
    } catch (error) {
        showMessage('Erro', 'Erro de conexão: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function carregarProdutos() {
    try {
        const response = await fetch(`${API_BASE_URL}/produtos`);
        const produtos = await response.json();
        
        const tbody = document.querySelector('#tabela-produtos tbody');
        tbody.innerHTML = '';
        
        produtos.forEach(produto => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${produto.codigo}</td>
                <td>${produto.nome}</td>
                <td>
                    <button class="btn btn-danger btn-small" onclick="deletarProduto(${produto.id})">
                        <i class="fas fa-trash"></i> Excluir
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Erro ao carregar produtos:', error);
    }
}

async function deletarProduto(id) {
    if (!confirm('Tem certeza que deseja excluir este produto? Todas as contagens relacionadas também serão excluídas.')) {
        return;
    }
    
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/produtos/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showMessage('Sucesso', 'Produto excluído com sucesso!', 'success');
            carregarProdutos();
            carregarContagens();
            carregarResumo();
        } else {
            const result = await response.json();
            showMessage('Erro', result.erro || 'Erro ao excluir produto', 'error');
        }
    } catch (error) {
        showMessage('Erro', 'Erro de conexão: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Funções de busca e contagem
async function handleBuscarProduto() {
    const codigo = document.getElementById('busca-codigo').value.trim();
    
    if (!codigo) {
        showMessage('Erro', 'Digite um código para buscar', 'error');
        return;
    }
    
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/produtos/${codigo}`);
        
        if (response.ok) {
            const produto = await response.json();
            mostrarProdutoEncontrado(produto);
        } else {
            const result = await response.json();
            showMessage('Erro', result.erro || 'Produto não encontrado', 'error');
            esconderProdutoEncontrado();
        }
    } catch (error) {
        showMessage('Erro', 'Erro de conexão: ' + error.message, 'error');
        esconderProdutoEncontrado();
    } finally {
        showLoading(false);
    }
}

function mostrarProdutoEncontrado(produto) {
    produtoAtual = produto;
    
    document.getElementById('produto-nome').textContent = produto.nome;
    document.getElementById('produto-codigo').textContent = produto.codigo;
    document.getElementById('produto-codigo-hidden').value = produto.codigo;
    
    document.getElementById('produto-encontrado').style.display = 'block';
    document.getElementById('card-contagem').style.display = 'block';
    
    // Limpar formulário de contagem
    document.getElementById('form-contagem').reset();
    document.getElementById('produto-codigo-hidden').value = produto.codigo;
}

function esconderProdutoEncontrado() {
    produtoAtual = null;
    document.getElementById('produto-encontrado').style.display = 'none';
    document.getElementById('card-contagem').style.display = 'none';
}

async function handleContagemSubmit(e) {
    e.preventDefault();
    
    if (!produtoAtual) {
        showMessage('Erro', 'Nenhum produto selecionado', 'error');
        return;
    }
    
    const formData = new FormData(e.target);
    const contagemData = {
        produto_codigo: produtoAtual.codigo,
        lote: formData.get('lote').trim(),
        validade_mes: parseInt(formData.get('validade_mes')),
        validade_ano: parseInt(formData.get('validade_ano')),
        quantidade: parseInt(formData.get('quantidade'))
    };
    
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/contagens`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(contagemData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            const acao = result.acao === 'atualizada' ? 'atualizada' : 'registrada';
            showMessage('Sucesso', `Contagem ${acao} com sucesso!`, 'success');
            e.target.reset();
            document.getElementById('produto-codigo-hidden').value = produtoAtual.codigo;
            carregarContagens();
            carregarResumo();
        } else {
            showMessage('Erro', result.erro || 'Erro ao registrar contagem', 'error');
        }
    } catch (error) {
        showMessage('Erro', 'Erro de conexão: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function carregarContagens() {
    try {
        const response = await fetch(`${API_BASE_URL}/contagens`);
        const contagens = await response.json();
        
        const tbody = document.querySelector('#tabela-contagens tbody');
        tbody.innerHTML = '';
        
        contagens.forEach(contagem => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${contagem.produto.codigo}</td>
                <td>${contagem.produto.nome}</td>
                <td>${contagem.lote}</td>
                <td>${contagem.validade_mes.toString().padStart(2, '0')}/${contagem.validade_ano}</td>
                <td>${contagem.quantidade}</td>
                <td>
                    <button class="btn btn-danger btn-small" onclick="deletarContagem(${contagem.id})">
                        <i class="fas fa-trash"></i> Excluir
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Erro ao carregar contagens:', error);
    }
}

async function deletarContagem(id) {
    if (!confirm('Tem certeza que deseja excluir esta contagem?')) {
        return;
    }
    
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/contagens/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showMessage('Sucesso', 'Contagem excluída com sucesso!', 'success');
            carregarContagens();
            carregarResumo();
        } else {
            const result = await response.json();
            showMessage('Erro', result.erro || 'Erro ao excluir contagem', 'error');
        }
    } catch (error) {
        showMessage('Erro', 'Erro de conexão: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Funções de relatório
async function carregarResumo() {
    const loadingElement = document.getElementById('resumo-loading');
    const tbody = document.querySelector('#tabela-resumo tbody');
    const totalElement = document.getElementById('total-geral');
    
    try {
        loadingElement.style.display = 'block';
        const response = await fetch(`${API_BASE_URL}/relatorio/resumo`);
        const data = await response.json();
        
        tbody.innerHTML = '';
        let totalGeral = 0;
        
        data.resumo.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.codigo}</td>
                <td>${item.nome}</td>
                <td>${item.total_quantidade}</td>
            `;
            tbody.appendChild(row);
            totalGeral += item.total_quantidade;
        });
        
        totalElement.textContent = totalGeral;
    } catch (error) {
        console.error('Erro ao carregar resumo:', error);
        showMessage('Erro', 'Erro ao carregar resumo do estoque', 'error');
    } finally {
        loadingElement.style.display = 'none';
    }
}

async function gerarRelatorio(tipo) {
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/relatorio/${tipo}`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            
            // Extrair nome do arquivo do cabeçalho Content-Disposition
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = `relatorio_estoque.${tipo}`;
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename="(.+)"/);
                if (filenameMatch) {
                    filename = filenameMatch[1];
                }
            }
            
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showMessage('Sucesso', `Relatório ${tipo.toUpperCase()} gerado com sucesso!`, 'success');
        } else {
            const result = await response.json();
            showMessage('Erro', result.erro || `Erro ao gerar relatório ${tipo.toUpperCase()}`, 'error');
        }
    } catch (error) {
        showMessage('Erro', 'Erro de conexão: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Funções de importação
async function baixarTemplate() {
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/template/produtos`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'template_produtos.xlsx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showMessage('Sucesso', 'Template baixado com sucesso!', 'success');
        } else {
            const result = await response.json();
            showMessage('Erro', result.erro || 'Erro ao baixar template', 'error');
        }
    } catch (error) {
        showMessage('Erro', 'Erro de conexão: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function importarExcel() {
    const fileInput = document.getElementById('arquivo-excel');
    const file = fileInput.files[0];
    
    if (!file) {
        showMessage('Erro', 'Selecione um arquivo Excel para importar', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('arquivo', file);
    
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/importar/produtos`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            mostrarResultadoImportacao(result);
            carregarProdutos();
            fileInput.value = '';
        } else {
            showMessage('Erro', result.erro || 'Erro ao importar arquivo', 'error');
        }
    } catch (error) {
        showMessage('Erro', 'Erro de conexão: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

function mostrarResultadoImportacao(resultado) {
    const resultadoDiv = document.getElementById('resultado-importacao');
    const detalhesDiv = document.getElementById('detalhes-importacao');
    
    let html = `
        <div class="import-stats">
            <div class="import-stat">
                <div class="number">${resultado.produtos_importados}</div>
                <div class="label">Importados</div>
            </div>
            <div class="import-stat">
                <div class="number">${resultado.produtos_duplicados}</div>
                <div class="label">Duplicados</div>
            </div>
            <div class="import-stat">
                <div class="number">${resultado.produtos_erro}</div>
                <div class="label">Erros</div>
            </div>
            <div class="import-stat">
                <div class="number">${resultado.total_processados}</div>
                <div class="label">Total</div>
            </div>
        </div>
    `;
    
    if (resultado.erros_detalhados && resultado.erros_detalhados.length > 0) {
        html += `
            <div class="import-errors">
                <h5>Erros encontrados:</h5>
                <ul>
                    ${resultado.erros_detalhados.map(erro => `<li>${erro}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    detalhesDiv.innerHTML = html;
    resultadoDiv.style.display = 'block';
    
    showMessage('Sucesso', resultado.mensagem, 'success');
}

// Funções utilitárias
function showMessage(title, message, type) {
    const modal = document.getElementById('modal');
    const modalBody = document.getElementById('modal-body');
    
    const iconClass = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle';
    const iconColor = type === 'success' ? '#27ae60' : '#e74c3c';
    
    modalBody.innerHTML = `
        <div style="text-align: center;">
            <i class="fas ${iconClass}" style="font-size: 3rem; color: ${iconColor}; margin-bottom: 20px;"></i>
            <h3 style="margin-bottom: 15px; color: #2c3e50;">${title}</h3>
            <p style="color: #7f8c8d; line-height: 1.5;">${message}</p>
        </div>
    `;
    
    modal.style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

function showLoading(show) {
    const overlay = document.getElementById('loading-overlay');
    overlay.style.display = show ? 'flex' : 'none';
}


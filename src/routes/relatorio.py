from flask import Blueprint, jsonify, request, send_file
from src.models.produto import Produto
from src.models.lote import Lote
from src.models.user import db
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import os

relatorio_bp = Blueprint('relatorio', __name__)

@relatorio_bp.route('/relatorio/excel', methods=['GET'])
def gerar_relatorio_excel():
    """Gera relatório de estoque em formato Excel"""
    try:
        # Buscar todos os produtos e seus lotes
        produtos = Produto.query.all()
        dados_relatorio = []
        
        for produto in produtos:
            lotes = Lote.query.filter_by(produto_codigo=produto.codigo).all()
            
            if lotes:
                # Produto com lotes
                for lote in lotes:
                    dados_relatorio.append({
                        'Código': produto.codigo,
                        'Nome do Produto': produto.nome,
                        'Lote': lote.lote,
                        'Validade': f"{lote.validade_mes:02d}/{lote.validade_ano}",
                        'Quantidade': lote.quantidade,
                        'Data Cadastro': lote.data_cadastro.strftime('%d/%m/%Y')
                    })
            else:
                # Produto sem lotes (quantidade zero)
                dados_relatorio.append({
                    'Código': produto.codigo,
                    'Nome do Produto': produto.nome,
                    'Lote': '-',
                    'Validade': '-',
                    'Quantidade': 0,
                    'Data Cadastro': '-'
                })
        
        # Criar DataFrame e salvar como Excel
        df = pd.DataFrame(dados_relatorio)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'relatorio_estoque_{timestamp}.xlsx'
        filepath = os.path.join('/tmp', filename)
        
        df.to_excel(filepath, index=False, sheet_name='Relatório de Estoque')
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar relatório Excel: {str(e)}'}), 500

@relatorio_bp.route('/relatorio/pdf', methods=['GET'])
def gerar_relatorio_pdf():
    """Gera relatório de estoque em formato PDF"""
    try:
        # Buscar todos os produtos e seus lotes
        produtos = Produto.query.all()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'relatorio_estoque_{timestamp}.pdf'
        filepath = os.path.join('/tmp', filename)
        
        # Criar documento PDF
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center
        )
        
        # Título
        title = Paragraph("Relatório de Estoque", title_style)
        elements.append(title)
        
        # Data de geração
        data_geracao = Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal'])
        elements.append(data_geracao)
        elements.append(Spacer(1, 20))
        
        # Dados da tabela
        data = [['Código', 'Nome do Produto', 'Lote', 'Validade', 'Qtd', 'Cadastro']]
        total_geral = 0
        
        for produto in produtos:
            lotes = Lote.query.filter_by(produto_codigo=produto.codigo).all()
            
            if lotes:
                subtotal = 0
                for lote in lotes:
                    data.append([
                        produto.codigo,
                        produto.nome,
                        lote.lote,
                        f"{lote.validade_mes:02d}/{lote.validade_ano}",
                        str(lote.quantidade),
                        lote.data_cadastro.strftime('%d/%m/%Y')
                    ])
                    subtotal += lote.quantidade
                
                # Adicionar subtotal
                data.append(['', '', '', '', f'Subtotal {produto.codigo}: {subtotal}', ''])
                total_geral += subtotal
            else:
                # Produto sem lotes
                data.append([produto.codigo, produto.nome, '-', '-', '0', '-'])
        
        # Total geral
        data.append(['', '', '', '', f'TOTAL GERAL: {total_geral}', ''])
        
        # Criar tabela
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        
        # Construir PDF
        doc.build(elements)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar relatório PDF: {str(e)}'}), 500

@relatorio_bp.route('/relatorio/resumo', methods=['GET'])
def get_resumo_estoque():
    """Retorna um resumo do estoque atual"""
    try:
        produtos = Produto.query.all()
        resumo = {
            'total_produtos': len(produtos),
            'produtos_com_estoque': 0,
            'produtos_sem_estoque': 0,
            'quantidade_total': 0,
            'total_lotes': 0
        }
        
        for produto in produtos:
            lotes = Lote.query.filter_by(produto_codigo=produto.codigo).all()
            quantidade_produto = sum(lote.quantidade for lote in lotes)
            
            if quantidade_produto > 0:
                resumo['produtos_com_estoque'] += 1
            else:
                resumo['produtos_sem_estoque'] += 1
            
            resumo['quantidade_total'] += quantidade_produto
            resumo['total_lotes'] += len(lotes)
        
        return jsonify(resumo)
        
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar resumo: {str(e)}'}), 500


from flask import Blueprint, request, jsonify, send_file
from src.models.user import db
from src.models.produto import Produto
from src.models.contagem import Contagem
from sqlalchemy import func
import pandas as pd
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime

relatorio_bp = Blueprint('relatorio', __name__)

@relatorio_bp.route('/relatorio/resumo', methods=['GET'])
def gerar_resumo():
    """Gera resumo das contagens agrupadas por produto"""
    try:
        # Query para buscar produtos com suas contagens
        query = db.session.query(
            Produto.codigo,
            Produto.nome,
            func.sum(Contagem.quantidade).label('total_quantidade')
        ).outerjoin(Contagem).group_by(Produto.id, Produto.codigo, Produto.nome).order_by(Produto.codigo)
        
        resultados = query.all()
        
        resumo = []
        total_geral = 0
        
        for resultado in resultados:
            quantidade = resultado.total_quantidade or 0
            total_geral += quantidade
            
            resumo.append({
                'codigo': resultado.codigo,
                'nome': resultado.nome,
                'total_quantidade': quantidade
            })
        
        return jsonify({
            'resumo': resumo,
            'total_geral': total_geral,
            'total_produtos': len(resumo),
            'data_geracao': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro ao gerar resumo: {str(e)}'}), 500

@relatorio_bp.route('/relatorio/detalhado', methods=['GET'])
def gerar_detalhado():
    """Gera relatório detalhado com todas as contagens"""
    try:
        # Query para buscar todas as contagens com produtos
        contagens = db.session.query(Contagem, Produto).join(Produto).order_by(Produto.codigo, Contagem.lote).all()
        
        detalhado = []
        for contagem, produto in contagens:
            detalhado.append({
                'codigo': produto.codigo,
                'nome': produto.nome,
                'lote': contagem.lote,
                'validade_mes': contagem.validade_mes,
                'validade_ano': contagem.validade_ano,
                'quantidade': contagem.quantidade
            })
        
        return jsonify({
            'detalhado': detalhado,
            'total_registros': len(detalhado),
            'data_geracao': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro ao gerar relatório detalhado: {str(e)}'}), 500

@relatorio_bp.route('/relatorio/excel', methods=['GET'])
def gerar_excel():
    """Gera relatório em formato Excel"""
    try:
        # Buscar dados do resumo
        query_resumo = db.session.query(
            Produto.codigo,
            Produto.nome,
            func.sum(Contagem.quantidade).label('total_quantidade')
        ).outerjoin(Contagem).group_by(Produto.id, Produto.codigo, Produto.nome).order_by(Produto.codigo)
        
        resumo_data = []
        total_geral = 0
        
        for resultado in query_resumo.all():
            quantidade = resultado.total_quantidade or 0
            total_geral += quantidade
            resumo_data.append({
                'Código': resultado.codigo,
                'Nome do Produto': resultado.nome,
                'Total Quantidade': quantidade
            })
        
        # Buscar dados detalhados
        contagens = db.session.query(Contagem, Produto).join(Produto).order_by(Produto.codigo, Contagem.lote).all()
        
        detalhado_data = []
        for contagem, produto in contagens:
            detalhado_data.append({
                'Código': produto.codigo,
                'Nome do Produto': produto.nome,
                'Lote': contagem.lote,
                'Mês Validade': contagem.validade_mes,
                'Ano Validade': contagem.validade_ano,
                'Quantidade': contagem.quantidade
            })
        
        # Criar arquivo Excel
        buffer = io.BytesIO()
        
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            # Aba Resumo
            df_resumo = pd.DataFrame(resumo_data)
            if not df_resumo.empty:
                df_resumo.to_excel(writer, sheet_name='Resumo', index=False)
                
                # Adicionar linha de total
                workbook = writer.book
                worksheet = writer.sheets['Resumo']
                
                # Adicionar total na última linha
                last_row = len(df_resumo) + 2
                worksheet[f'A{last_row}'] = 'TOTAL GERAL'
                worksheet[f'C{last_row}'] = total_geral
                
                # Formatação
                from openpyxl.styles import Font, PatternFill
                bold_font = Font(bold=True)
                yellow_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
                
                worksheet[f'A{last_row}'].font = bold_font
                worksheet[f'C{last_row}'].font = bold_font
                worksheet[f'A{last_row}'].fill = yellow_fill
                worksheet[f'C{last_row}'].fill = yellow_fill
                
                # Ajustar largura das colunas
                worksheet.column_dimensions['A'].width = 15
                worksheet.column_dimensions['B'].width = 40
                worksheet.column_dimensions['C'].width = 15
            
            # Aba Detalhado
            df_detalhado = pd.DataFrame(detalhado_data)
            if not df_detalhado.empty:
                df_detalhado.to_excel(writer, sheet_name='Detalhado', index=False)
                
                # Ajustar largura das colunas
                worksheet_det = writer.sheets['Detalhado']
                worksheet_det.column_dimensions['A'].width = 15
                worksheet_det.column_dimensions['B'].width = 40
                worksheet_det.column_dimensions['C'].width = 15
                worksheet_det.column_dimensions['D'].width = 12
                worksheet_det.column_dimensions['E'].width = 12
                worksheet_det.column_dimensions['F'].width = 15
        
        buffer.seek(0)
        
        # Nome do arquivo com timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'relatorio_estoque_{timestamp}.xlsx'
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        return jsonify({'erro': f'Erro ao gerar Excel: {str(e)}'}), 500

@relatorio_bp.route('/relatorio/pdf', methods=['GET'])
def gerar_pdf():
    """Gera relatório em formato PDF"""
    try:
        # Buscar dados
        query_resumo = db.session.query(
            Produto.codigo,
            Produto.nome,
            func.sum(Contagem.quantidade).label('total_quantidade')
        ).outerjoin(Contagem).group_by(Produto.id, Produto.codigo, Produto.nome).order_by(Produto.codigo)
        
        resumo_data = []
        total_geral = 0
        
        for resultado in query_resumo.all():
            quantidade = resultado.total_quantidade or 0
            total_geral += quantidade
            resumo_data.append([resultado.codigo, resultado.nome, str(quantidade)])
        
        # Criar PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Centralizado
        )
        
        # Conteúdo
        story = []
        
        # Título
        title = Paragraph("Relatório de Estoque", title_style)
        story.append(title)
        
        # Data de geração
        data_geracao = datetime.now().strftime('%d/%m/%Y às %H:%M')
        data_para = Paragraph(f"Gerado em: {data_geracao}", styles['Normal'])
        story.append(data_para)
        story.append(Spacer(1, 20))
        
        # Tabela de dados
        if resumo_data:
            # Cabeçalho da tabela
            table_data = [['Código', 'Nome do Produto', 'Quantidade']]
            table_data.extend(resumo_data)
            
            # Linha de total
            table_data.append(['', 'TOTAL GERAL', str(total_geral)])
            
            # Criar tabela
            table = Table(table_data, colWidths=[1.5*inch, 4*inch, 1.5*inch])
            
            # Estilo da tabela
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.yellow),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
        else:
            no_data = Paragraph("Nenhum dado encontrado.", styles['Normal'])
            story.append(no_data)
        
        # Gerar PDF
        doc.build(story)
        buffer.seek(0)
        
        # Nome do arquivo com timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'relatorio_estoque_{timestamp}.pdf'
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'erro': f'Erro ao gerar PDF: {str(e)}'}), 500


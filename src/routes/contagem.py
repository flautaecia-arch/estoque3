from flask import Blueprint, jsonify, request
from src.models.produto import Produto
from src.models.lote import Lote
from src.models.user import db
from sqlalchemy.exc import IntegrityError

contagem_bp = Blueprint('contagem', __name__)

@contagem_bp.route('/contagem', methods=['POST'])
def registrar_contagem():
    """Registra uma nova contagem de lote ou atualiza uma existente"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    produto_codigo = data.get('produto_codigo')
    lote_nome = data.get('lote')
    validade_mes = data.get('validade_mes')
    validade_ano = data.get('validade_ano')
    quantidade = data.get('quantidade')
    
    # Validação dos dados
    if not all([produto_codigo, lote_nome, validade_mes, validade_ano]):
        return jsonify({'error': 'Campos obrigatórios: produto_codigo, lote, validade_mes, validade_ano'}), 400
    
    if quantidade is None or quantidade < 0:
        return jsonify({'error': 'Quantidade deve ser um número não negativo'}), 400
    
    # Verificar se o produto existe
    produto = Produto.query.get(produto_codigo)
    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    try:
        # Verificar se o lote já existe para este produto
        lote_existente = Lote.query.filter_by(produto_codigo=produto_codigo, lote=lote_nome).first()
        
        if lote_existente:
            # Se existe, somar a quantidade
            lote_existente.quantidade += quantidade
            db.session.commit()
            return jsonify({
                'message': 'Quantidade adicionada ao lote existente',
                'lote': lote_existente.to_dict()
            })
        else:
            # Se não existe, criar novo lote
            novo_lote = Lote(
                produto_codigo=produto_codigo,
                lote=lote_nome,
                validade_mes=validade_mes,
                validade_ano=validade_ano,
                quantidade=quantidade
            )
            db.session.add(novo_lote)
            db.session.commit()
            return jsonify({
                'message': 'Novo lote registrado com sucesso',
                'lote': novo_lote.to_dict()
            }), 201
            
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Erro ao registrar lote'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@contagem_bp.route('/contagem/lotes/<produto_codigo>', methods=['GET'])
def get_lotes_produto(produto_codigo):
    """Retorna todos os lotes de um produto específico"""
    produto = Produto.query.get(produto_codigo)
    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    lotes = Lote.query.filter_by(produto_codigo=produto_codigo).all()
    return jsonify([lote.to_dict() for lote in lotes])


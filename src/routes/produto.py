from flask import Blueprint, jsonify, request
from src.models.produto import Produto
from src.models.lote import Lote
from src.models.user import db

produto_bp = Blueprint('produto', __name__)

@produto_bp.route('/api/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{
        'id': p.id,
        'codigo': p.codigo,
        'nome': p.nome
    } for p in produtos])

@produto_bp.route('/api/produtos/<codigo>', methods=['GET'])
def buscar_produto(codigo):
    produto = Produto.query.filter_by(codigo=codigo).first()
    if produto:
        return jsonify({
            'id': produto.id,
            'codigo': produto.codigo,
            'nome': produto.nome
        })
    return jsonify({'error': 'Produto não encontrado'}), 404

@produto_bp.route('/api/produtos', methods=['POST'])
def adicionar_produto():
    try:
        data = request.get_json()
        
        if not data or 'codigo' not in data or 'nome' not in data:
            return jsonify({'error': 'Código e nome são obrigatórios'}), 400
        
        codigo = data['codigo'].strip()
        nome = data['nome'].strip()
        
        if not codigo or not nome:
            return jsonify({'error': 'Código e nome não podem estar vazios'}), 400
        
        # Verificar se já existe produto com este código
        produto_existente = Produto.query.filter_by(codigo=codigo).first()
        if produto_existente:
            return jsonify({'error': 'Já existe um produto com este código'}), 409
        
        # Criar novo produto
        novo_produto = Produto(codigo=codigo, nome=nome)
        db.session.add(novo_produto)
        db.session.commit()
        
        return jsonify({
            'id': novo_produto.id,
            'codigo': novo_produto.codigo,
            'nome': novo_produto.nome,
            'message': 'Produto adicionado com sucesso'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@produto_bp.route('/api/produtos/<codigo>', methods=['PUT'])
def editar_produto(codigo):
    try:
        produto = Produto.query.filter_by(codigo=codigo).first()
        if not produto:
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Atualizar nome se fornecido
        if 'nome' in data:
            nome = data['nome'].strip()
            if not nome:
                return jsonify({'error': 'Nome não pode estar vazio'}), 400
            produto.nome = nome
        
        # Atualizar código se fornecido
        if 'codigo' in data:
            novo_codigo = data['codigo'].strip()
            if not novo_codigo:
                return jsonify({'error': 'Código não pode estar vazio'}), 400
            
            # Verificar se o novo código já existe (exceto para o produto atual)
            produto_existente = Produto.query.filter_by(codigo=novo_codigo).first()
            if produto_existente and produto_existente.id != produto.id:
                return jsonify({'error': 'Já existe um produto com este código'}), 409
            
            produto.codigo = novo_codigo
        
        db.session.commit()
        
        return jsonify({
            'id': produto.id,
            'codigo': produto.codigo,
            'nome': produto.nome,
            'message': 'Produto atualizado com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@produto_bp.route('/api/produtos/<codigo>', methods=['DELETE'])
def excluir_produto(codigo):
    try:
        produto = Produto.query.filter_by(codigo=codigo).first()
        if not produto:
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        # Verificar se existem lotes associados ao produto
        lotes_associados = Lote.query.filter_by(produto_id=produto.id).count()
        if lotes_associados > 0:
            return jsonify({
                'error': f'Não é possível excluir o produto. Existem {lotes_associados} lote(s) associado(s) a este produto.'
            }), 409
        
        # Excluir produto
        db.session.delete(produto)
        db.session.commit()
        
        return jsonify({
            'message': f'Produto {codigo} - {produto.nome} excluído com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

# Manter compatibilidade com rotas antigas
@produto_bp.route('/produtos', methods=['GET'])
def get_produtos():
    """Retorna todos os produtos cadastrados"""
    produtos = Produto.query.all()
    return jsonify([produto.to_dict() for produto in produtos])

@produto_bp.route('/produtos/<codigo>', methods=['GET'])
def get_produto(codigo):
    """Retorna um produto específico pelo código"""
    produto = Produto.query.filter_by(codigo=codigo).first()
    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    # Buscar lotes do produto
    lotes = Lote.query.filter_by(produto_id=produto.id).all()
    produto_dict = produto.to_dict()
    produto_dict['lotes'] = [lote.to_dict() for lote in lotes]
    produto_dict['quantidade_total'] = sum(lote.quantidade for lote in lotes)
    
    return jsonify(produto_dict)

@produto_bp.route('/produtos/buscar/<codigo>', methods=['GET'])
def buscar_produto_compat(codigo):
    """Busca um produto pelo código (compatibilidade)"""
    return get_produto(codigo)


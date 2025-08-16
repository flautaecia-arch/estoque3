from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.produto import Produto
from src.models.contagem import Contagem
from sqlalchemy.exc import IntegrityError

contagem_bp = Blueprint('contagem', __name__)

@contagem_bp.route('/contagens', methods=['GET'])
def listar_contagens():
    """Lista todas as contagens com informações do produto"""
    contagens = db.session.query(Contagem, Produto).join(Produto).all()
    resultado = []
    for contagem, produto in contagens:
        item = contagem.to_dict()
        item['produto'] = produto.to_dict()
        resultado.append(item)
    return jsonify(resultado)

@contagem_bp.route('/contagens', methods=['POST'])
def registrar_contagem():
    """Registra uma nova contagem ou atualiza existente"""
    data = request.get_json()
    
    # Validar dados obrigatórios
    campos_obrigatorios = ['produto_codigo', 'lote', 'validade_mes', 'validade_ano', 'quantidade']
    for campo in campos_obrigatorios:
        if campo not in data:
            return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
    
    # Buscar produto pelo código
    produto = Produto.query.filter_by(codigo=data['produto_codigo']).first()
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    # Validar dados
    try:
        validade_mes = int(data['validade_mes'])
        validade_ano = int(data['validade_ano'])
        quantidade = int(data['quantidade'])
        
        if not (1 <= validade_mes <= 12):
            return jsonify({'erro': 'Mês de validade deve estar entre 1 e 12'}), 400
        
        if validade_ano < 2020 or validade_ano > 2050:
            return jsonify({'erro': 'Ano de validade deve estar entre 2020 e 2050'}), 400
            
        if quantidade < 0:
            return jsonify({'erro': 'Quantidade não pode ser negativa'}), 400
            
    except ValueError:
        return jsonify({'erro': 'Validade e quantidade devem ser números'}), 400
    
    # Verificar se já existe contagem para este produto e lote
    contagem_existente = Contagem.query.filter_by(
        produto_id=produto.id,
        lote=data['lote'].strip()
    ).first()
    
    if contagem_existente:
        # Atualizar contagem existente (somar quantidade)
        contagem_existente.quantidade += quantidade
        contagem_existente.validade_mes = validade_mes
        contagem_existente.validade_ano = validade_ano
        db.session.commit()
        
        resultado = contagem_existente.to_dict()
        resultado['produto'] = produto.to_dict()
        resultado['acao'] = 'atualizada'
        return jsonify(resultado)
    else:
        # Criar nova contagem
        nova_contagem = Contagem(
            produto_id=produto.id,
            lote=data['lote'].strip(),
            validade_mes=validade_mes,
            validade_ano=validade_ano,
            quantidade=quantidade
        )
        db.session.add(nova_contagem)
        db.session.commit()
        
        resultado = nova_contagem.to_dict()
        resultado['produto'] = produto.to_dict()
        resultado['acao'] = 'criada'
        return jsonify(resultado), 201

@contagem_bp.route('/contagens/produto/<codigo>', methods=['GET'])
def listar_contagens_produto(codigo):
    """Lista todas as contagens de um produto específico"""
    produto = Produto.query.filter_by(codigo=codigo).first()
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    contagens = Contagem.query.filter_by(produto_id=produto.id).all()
    resultado = []
    for contagem in contagens:
        item = contagem.to_dict()
        item['produto'] = produto.to_dict()
        resultado.append(item)
    
    return jsonify(resultado)

@contagem_bp.route('/contagens/<int:contagem_id>', methods=['DELETE'])
def deletar_contagem(contagem_id):
    """Deleta uma contagem específica"""
    contagem = Contagem.query.get_or_404(contagem_id)
    db.session.delete(contagem)
    db.session.commit()
    return jsonify({'mensagem': 'Contagem deletada com sucesso'})

@contagem_bp.route('/contagens/<int:contagem_id>', methods=['PUT'])
def atualizar_contagem(contagem_id):
    """Atualiza uma contagem específica"""
    contagem = Contagem.query.get_or_404(contagem_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'erro': 'Dados não fornecidos'}), 400
    
    try:
        if 'lote' in data:
            contagem.lote = data['lote'].strip()
        if 'validade_mes' in data:
            mes = int(data['validade_mes'])
            if not (1 <= mes <= 12):
                return jsonify({'erro': 'Mês de validade deve estar entre 1 e 12'}), 400
            contagem.validade_mes = mes
        if 'validade_ano' in data:
            ano = int(data['validade_ano'])
            if ano < 2020 or ano > 2050:
                return jsonify({'erro': 'Ano de validade deve estar entre 2020 e 2050'}), 400
            contagem.validade_ano = ano
        if 'quantidade' in data:
            qtd = int(data['quantidade'])
            if qtd < 0:
                return jsonify({'erro': 'Quantidade não pode ser negativa'}), 400
            contagem.quantidade = qtd
        
        db.session.commit()
        
        resultado = contagem.to_dict()
        produto = Produto.query.get(contagem.produto_id)
        resultado['produto'] = produto.to_dict()
        return jsonify(resultado)
        
    except ValueError:
        return jsonify({'erro': 'Validade e quantidade devem ser números'}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'erro': 'Já existe uma contagem para este produto e lote'}), 409


from flask import Blueprint, render_template, request, redirect, url_for, make_response, flash

produtos_blueprint = Blueprint('produtos', __name__)

produtos = []

@produtos_blueprint.route('/produtos', methods=['GET'])
def listar_produtos():
    return render_template('produtos.html', produtos=produtos)

@produtos_blueprint.route('/adicionar_ao_carrinho/<int:produto_id>', methods=['POST'])
def adicionar_ao_carrinho(produto_id):
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto:
        resp = make_response(redirect(url_for('produtos.listar_produtos')))
        carrinho = request.cookies.get('carrinho')
        if not carrinho:
            carrinho = str(produto_id)
        else:
            carrinho += f',{produto_id}'
        resp.set_cookie('carrinho', carrinho)
        flash('Produto adicionado ao carrinho!', 'success')
        return resp
    else:
        flash('Produto não encontrado!', 'error')
        return redirect(url_for('produtos.listar_produtos'))

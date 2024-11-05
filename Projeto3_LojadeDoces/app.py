from flask import Flask, session, redirect, url_for, flash, request, render_template, make_response
from controllers.auth import auth_blueprint
from controllers.produtos import produtos_blueprint

app = Flask(__name__)
app.secret_key = 'doce-delicioso'
app.config['doce-gostoso'] = 'session'

app.register_blueprint(auth_blueprint)
app.register_blueprint(produtos_blueprint)

@app.route('/')
def index():
    if 'usuario' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'error')
        return redirect(url_for('auth.login'))
    
    return render_template('index.html')

@app.route('/carrinho')
def carrinho():
    carrinho = request.cookies.get('carrinho')
    if carrinho:
        produtos = carrinho.split(',')
    else:
        produtos = []

    return render_template('carrinho.html', produtos=produtos)

@app.route('/adicionar_ao_carrinho/<produto>')
def adicionar_ao_carrinho(produto):
    carrinho = request.cookies.get('carrinho')
    if carrinho:
        produtos = carrinho.split(',')
        if produto not in produtos:
            produtos.append(produto)
    else:
        produtos = [produto]
    
    resposta = make_response(redirect(url_for('index')))
    resposta.set_cookie('carrinho', ','.join(produtos), max_age=60*60*24)
    flash(f'{produto} adicionado ao carrinho!', 'success')
    return resposta

@app.route('/remover_do_carrinho/<produto>', methods=['POST'])
def remover_do_carrinho(produto):
    carrinho = request.cookies.get('carrinho')
    if carrinho:
        produtos = carrinho.split(',')
        if produto in produtos:
            produtos.remove(produto)
            resposta = make_response(redirect(url_for('carrinho')))
            if produtos:
                resposta.set_cookie('carrinho', ','.join(produtos), max_age=60*60*24)
            else:
                resposta.set_cookie('carrinho', '', expires=0)
            flash(f'{produto} removido do carrinho!', 'success')
        else:
            flash(f'O produto "{produto}" não está no carrinho.', 'error')
    else:
        flash('O carrinho está vazio.', 'error')

    return resposta

@app.errorhandler(401)
def erro_401(e):
    return render_template('erro_401.html'), 401

@app.errorhandler(403)
def erro_403(e):
    return render_template('erro_403.html'), 403

@app.errorhandler(404)
def erro_404(e):
    return render_template('erro_404.html'), 404

@app.errorhandler(500)
def erro_500(e):
    return render_template('erro_500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_blueprint = Blueprint('auth', __name__)

usuarios = {'usuario': 'senha123'}

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario in usuarios and usuarios[usuario] == senha:
            session['usuario'] = usuario
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos!', 'error')
    return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Você foi desconectado com sucesso.', 'success')
    return redirect(url_for('auth.login'))

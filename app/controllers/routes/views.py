from flask import render_template, request, Blueprint, url_for, redirect, current_app
from flask_login import login_required, login_user, logout_user, current_user
from passlib.hash import pbkdf2_sha256

from app.controllers.forms.forms import *
from app.controllers.functions.email import enviar_email_dm
from app.controllers.functions.helpers import *
from app.controllers.constants import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(current_app, key_func=get_remote_address)
views = Blueprint('views', __name__, static_folder='static', template_folder='templates')


@views.route('/', methods=["GET", "POST"])
def index():
    """
    Renderiza a página inicial do projeto
    """
    form_login = LoginForm(request.form)
    return render_template('views/index.html', title='Página inicial',
                           secomp_now=secomp_now[0], secomp=secomp[0],
                           secomp_email=secomp_email,
                           secompEdition=secomp_edition,
                           form_login=form_login)


@views.route('/contato', methods=['POST', 'GET'])
def contato_dm():
    """
    Página de contato
    """
    form = ContatoForm(request.form)
    form_login = LoginForm(request.form)
    if form.validate_on_submit():
        nome = form.nome_completo.data
        email = form.email.data
        mensagem = form.mensagem.data
        enviar_email_dm(nome, email, mensagem)
        return render_template('views/contato.html', form=form, enviado=True, form_login=form_login)
    return render_template('views/contato.html', form=form, form_login=form_login)


@views.route('/constr', methods=["GET", "POST"])
def constr():
    form_login = LoginForm(request.form)
    return render_template('views/em_constr.html', title='Página em construção', form_login=form_login)


@views.route('/sobre', methods=["GET", "POST"])
def sobre():
    form_login = LoginForm(request.form)
    return render_template('views/sobre.html', title='Sobre a Secomp', form_login=form_login)


@views.route('/cronograma', methods=["GET", "POST"])
def cronograma():
    form_login = LoginForm(request.form)
    return render_template('views/cronograma.html', title='Cronograma', form_login=form_login)


@views.route('/equipe', methods=["GET", "POST"])
def equipe():
    form_login = LoginForm(request.form)
    return render_template('views/equipe.html', title='Equipe', data=get_equipe(), form_login=form_login)


@views.route('/faq', methods=["GET", "POST"])
def faq():
    form_login = LoginForm(request.form)
    return render_template('views/faq.html', title='FAQ', form_login=form_login)


@views.route('/ctf', methods=["GET", "POST"])
def ctf():
    form_login = LoginForm(request.form)
    return render_template('views/ctf.html', title='CTF', form_login=form_login)

#@views.route('/gamejam', methods=["GET", "POST"])
def gamejam():
    form_login = LoginForm(request.form)
    return render_template('views/gamejam.html', title='CTF', form_login=form_login)

@views.route('/teste', methods=["GET","POST"])
def teste():
    form_login = LoginForm(request.form)
    return render_template('teste.html', title='Teste', form_login=form_login)

@limiter.limit("50/day")
@views.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = db.session.query(Usuario).filter_by(
            email=form.email.data).first()
        if user:
            atividade_confirmada, atividade, view_atividade = confirmacao_atividade_ministrante(user)
            if user.senha is not None and pbkdf2_sha256.verify(form.senha.data, user.senha):
                user.autenticado = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                if atividade_confirmada == False:
                    return redirect(url_for('conteudo.dados_hospedagem_transporte'))
                return redirect(url_for('users.dashboard'))
        return render_template('views/login.html', form=form, erro=True)
    return render_template('views/login.html', form=form)


@views.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    Renderiza a página de logout do projeto
    """
    user = current_user
    user.autenticado = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('.index'))

@views.route("/senhas", methods=["GET"])
def senhas():
    return render_template('views/requisito_50.html')

@views.route("/patrocinadores", methods=["GET"])
def patrocinadores():
    '''
    Renderiza página referente aos patrocinadores da edição atual
    '''
    form = LoginForm(request.form)
    patrocinadores = db.session.query(Patrocinador).filter_by(ativo_site=True).order_by(Patrocinador.id_cota)
    return render_template('views/patrocinadores.html', patrocinadores=patrocinadores, form_login=form, edicao=EDICAO_ATUAL)

@views.route("/pontuacao", methods=["GET"])
def pontuacao_compcases():
    '''
    Renderiza página referente a pontuação geral do COMPCases
    '''
    form = LoginForm(request.form)
    participantes = get_ranking_pontuacao()
    participante_logado = None
    try:
        participante_logado = participante = db.session.query(Participante).filter_by(
            usuario=current_user).first()
    except:
        pass
    return render_template('views/pontuacao_compcases.html', participantes=participantes, participante_logado=participante_logado, form_login=form)
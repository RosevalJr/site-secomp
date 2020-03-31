import magic

from time import strftime, gmtime

from flask import url_for, render_template, current_app
from flask_login import current_user
from flask_mail import Mail, Message

from app.models.models import db, Usuario
from app.controllers.functions.helpers import get_usuarios_query, get_path_anexo

mail = Mail()

_teste = {
    "assunto": "Teste",  # assunto do email
    "nome": "Pessoa",  # nome do destinatário
    "titulo": "EMAIL TESTE",
    "email": "ti@secompufscar.com.br",  # email destino
    "template": "email/teste.html",  # path do template (raiz dentro do diretório 'templates')
    "footer": "TI X SECOMP UFSCar",
}


def enviar_email_generico(info=None, anexo=None):
    """
    Função que envia um email genérico recebendo um dicionário, que deve ter dados obrigatórios
    (ver dicionario teste) mas pode ter dados a mais a serem passados para o template
    Por padrão a chamada da função sem argumentos enviará um email teste para o ti
    """
    if info is None:
        global _teste
        info = _teste
    msg = Message(
        info["assunto"], sender=("SECOMP UFSCar", str(current_app.config["DEFAULT_MAIL_SENDER"])), recipients=[info["email"]]
    )

    try:
        msg.html = render_template(info["template"], info=info)

        # Parte que cuida dos anexos
        if not (anexo is None or anexo == []):
            for fileName in anexo:
                try:
                    mimetype = magic.from_file(fileName, mime=True)
                    with open(fileName, "rb") as fp:
                        try:
                            msg.attach(fileName, mimetype, fp.read())
                        except Exception as e:
                            print("Erro no anexo. {}".format(e))
                            return (info, e)
                except Exception as e:
                    print("Erro ao abrir arquivo do anexo. {}".format(e))
                    return (info, e)

    except Exception as e:
        print("Erro no template. {}".format(e))
        return (info, e)

    try:
        global mail
        mail.send(msg)
    except Exception as e:  # Erros mais prováveis são devido ao email_config, printa error em um arquivo
        try:
            log = open("logMailError.txt", "a+")
            log.write(f"{str(e)} {info['email']} {strftime('%a, %d %b %Y %H:%M:%S', gmtime())}\n")
            log.close()
        except Exception:
            return (info, e)


def enviar_email_confirmacao(usuario, token):
    """
    Envia email para validação do email
    """
    # Cria a msg, Assunto, De, Para
    link = url_for("participantes.verificacao", token=token, _external=True)
    info = {
        "assunto": "Confirmação de Email",
        "nome": usuario.primeiro_nome,
        "titulo": "CONFIRMAÇÃO DE EMAIL",
        "email": usuario.email,
        "template": "email/confirmacao_de_email.html",
        "link": str(link),
        "footer": "TI X SECOMP UFSCar",
    }
    enviar_email_generico(info)


def enviar_email_dm(nome, email, mensagem):
    msg = Message(f"Mensagem de {nome}", sender=current_app.config["MAIL_USERNAME"], recipients=current_app.config["MAIL_DM"])
    msg.body = f"{nome}\nEmail: {email}\n\n{mensagem}"

    try:
        global mail
        mail.send(msg)  # Envia o email
    except Exception as e:  # Erros mais prováveis são devivo ao email_config, printa error em um arquivo
        try:
            log = open("logMailError.txt", "a+")
            log.write(f'{str(e)} {email} {strftime("%a, %d %b %Y %H:%M:%S", gmtime())}\n')
            log.close()
        except Exception:
            return


def enviar_email_senha(usuario, token):
    """
    Envia email para alteração de senha
    """
    # Cria a Msg, Assunto, De, Para
    link = url_for("participantes.confirmar_alteracao_senha", token=token, _external=True)
    info = {
        "assunto": "Alteração de Senha",
        "nome": usuario.primeiro_nome,
        "titulo": "ALTERAÇÃO DE SENHA",
        "email": usuario.email,
        "template": "email/alteracao_senha.html",
        "link": str(link),
        "footer": "TI X SECOMP UFSCar",
    }
    enviar_email_generico(info)


def email_confirmado():
    try:
        usuario = current_user
        usuario = db.session.query(Usuario).filter_by(email=usuario.email).first()
        return usuario.email_verificado
    except Exception as e:
        print(e)
        return None


def enviar_email_custon(assunto, titulo, template, temAnexo, anexoBase, anexoPasta, complemento, selecionados, extencao):
    """
    Envia um ou mais emails customizados
    Podendo ou não ter anexo
    """
    usuarios = get_usuarios_query()

    naoEnviados = []

    for i in selecionados:
        usuario = usuarios.filter_by(id=i).first()

        info = {
            "assunto": assunto,
            "nome": usuario.primeiro_nome,
            "titulo": titulo,
            "email": usuario.email,
            "template": "email/" + template,
            "footer": "TI X SECOMP UFSCar",
        }

        # Verifica a existencia de anexo
        if temAnexo:
            files = []
            files.append(get_path_anexo(anexoBase, anexoPasta, complemento, usuario, extencao))

            temp = enviar_email_generico(info, files)

            # Cria a lista de erros
            if not (temp == None or temp == []):
                naoEnviados.append(temp)
        else:
            temp = enviar_email_generico(info, None)

            # Cria a lista de erros
            if not (temp == None or temp == []):
                naoEnviados.append(temp)

    return naoEnviados


def enviar_email_aviso_pagamento_kit_aprovado(usuario):
    """
    Envia email para validação do email
    """
    info = {
        "assunto": "Pagamento do KIT da X SECOMP UFSCar",
        "nome": usuario.primeiro_nome,
        "titulo": "COMPROVANTE APROVADO",
        "email": usuario.email,
        "template": "email/pagamento_kit_aprovado.html",
        "footer": "TI X SECOMP UFSCar",
    }
    enviar_email_generico(info)


def enviar_email_aviso_pagamento_kit_rejeitado(usuario):
    """
    Envia email para validação do email
    """
    info = {
        "assunto": "Pagamento do KIT da X SECOMP UFSCar",
        "nome": usuario.primeiro_nome,
        "titulo": "COMPROVANTE NÃO APROVADO",
        "email": usuario.email,
        "template": "email/pagamento_kit_rejeitado.html",
        "footer": "TI X SECOMP UFSCar",
    }
    enviar_email_generico(info)


def enviar_email_aviso_sucesso_confirmacao_pagamento_paypal(usuario, pagamento):
    """
    Envia email para validação do email
    """
    info = {
        "assunto": "Pagamento do KIT da X SECOMP UFSCar",
        "nome": usuario.primeiro_nome,
        "titulo": "PAGAMENTO CONFIRMADO",
        "email": usuario.email,
        "valor": "{:2.2f}".format(pagamento.valor).replace(".", ","),
        "template": "email/pagamento_kit_confirmado.html",
        "footer": "TI X SECOMP UFSCar",
    }
    enviar_email_generico(info)


def enviar_email_aviso_inscricao(usuario):
    """
    Envia email para validação do email
    """
    info = {
        "assunto": "Complete sua inscrição em nosso site",
        "nome": usuario.primeiro_nome,
        "titulo": "AVISO DE INSCRIÇÃO",
        "email": usuario.email,
        "template": "email/email_aviso_inscricao.html",
        "footer": "TI X SECOMP UFSCar",
    }
    enviar_email_generico(info)


def enviar_email_aviso_tolerancia(usuario):
    """
    Envia email de aviso de tolerância
    """
    info = {
        "assunto": "Aviso de tolerância de atraso",
        "nome": usuario.primeiro_nome,
        "titulo": "AVISO DE TOLERÂNCIA DE ATRASO",
        "email": usuario.email,
        "template": "email/aviso_tolerancia.html",
        "footer": "TI X SECOMP UFSCar",
    }
    enviar_email_generico(info)


def enviar_email_feedback(usuario):
    """
    Envia email para validação do email
    """
    info = {
        "assunto": "Feedback X SECOMP UFSCar",
        "nome": usuario.primeiro_nome,
        "titulo": "FEEDBACK X SECOMP UFSCar",
        "email": usuario.email,
        "template": "email/feedback.html",
        "footer": "TI X SECOMP UFSCar",
    }
    enviar_email_generico(info)

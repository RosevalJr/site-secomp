from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, DateField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from app.controllers.functions import get_opcoes_cidades, get_opcoes_instituicoes, get_opcoes_cursos, get_opcoes_camisetas
from app.controllers.constants import *


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message=ERRO_INPUT_REQUIRED), Email(message=ERRO_EMAIL), Length(min=1, max=254)])
    senha = PasswordField('Senha', validators=[InputRequired(message=ERRO_INPUT_REQUIRED), Length(min=8, max=20, message=ERRO_TAMANHO_SENHA)])

class CadastroForm(FlaskForm):
    primeiro_nome = StringField('Primeiro Nome', validators=[InputRequired(message=ERRO_INPUT_REQUIRED), Length(min=1, max=30)])
    sobrenome = StringField('Sobrenome', validators=[InputRequired(message=ERRO_INPUT_REQUIRED), Length(min=1, max=100)])
    email = StringField('Email', validators=[InputRequired(message=ERRO_INPUT_REQUIRED), Email(message=ERRO_EMAIL), Length(min=1, max=254)])
    senha = PasswordField('Senha', validators=[InputRequired(message=ERRO_INPUT_REQUIRED), EqualTo('confirmacao', message=ERRO_COMPARA_SENHAS), Length(min=8, max=20, message=ERRO_TAMANHO_SENHA)])
    confirmacao = PasswordField('Confirmação de Senha', validators=[InputRequired(message=ERRO_INPUT_REQUIRED), Length(min=8, max=20)])
    curso = SelectField('Curso', choices=get_opcoes_cursos(), id= "curso", coerce=int)
    instituicao = SelectField('Instituição', choices=get_opcoes_instituicoes(), id="instituicao", default="UFSCar", coerce=int)
    cidade = SelectField('Cidade', choices=get_opcoes_cidades(), id="cidade", default="São Carlos", coerce=int)
    data_nasc = DateField("Data de Nascimento", format="%d/%m/%Y", id="data_nasc")

class ParticipanteForm(FlaskForm):
    kit = BooleanField('Kit', validators=[InputRequired()], id="kit")
    camiseta = SelectField('Camiseta', choices=get_opcoes_camisetas(), id= "camiseta", default="P Feminino", coerce=int)
    restricao_coffee = SelectField('Restrição para o Coffee-Break', choices=escolhas_restricao, default="Nenhum", coerce=int )

class EditarUsuarioForm(FlaskForm):
    primeiro_nome = StringField('Primeiro Nome', validators=[InputRequired(message=ERRO_INPUT_REQUIRED), Length(min=1, max=30)])
    sobrenome = StringField('Sobrenome', validators=[InputRequired(message=ERRO_INPUT_REQUIRED), Length(min=1, max=100)])
    email = StringField('Email', validators=[InputRequired(message=ERRO_INPUT_REQUIRED), Email(message=ERRO_EMAIL), Length(min=1, max=254)])
    curso = SelectField('Curso', choices=get_opcoes_cursos(), id= 'curso', coerce=int)
    instituicao = SelectField('Instituição', choices=get_opcoes_instituicoes(), id='instituicao', coerce=int)
    cidade = SelectField('Cidade', choices=get_opcoes_cidades(), id='cidade', coerce=int)
    data_nasc = DateField("Data de Nascimento", format="%d/%m/%Y", id='data-nasc')
    senha = PasswordField('Senha', validators=[InputRequired(message=ERRO_INPUT_REQUIRED), Length(min=8, max=20, message=ERRO_TAMANHO_SENHA)])

class AlterarSenhaForm(FlaskForm):
    nova_senha = PasswordField('Senha', validators=[InputRequired(message=ERRO_INPUT_REQUIRED), Length(min=8, max=20, message=ERRO_TAMANHO_SENHA), EqualTo('confirmacao', message=ERRO_COMPARA_SENHAS)])
    confirmacao = PasswordField('Confirmação de Senha', validators=[InputRequired(message=ERRO_INPUT_REQUIRED), Length(min=8, max=20)])

class AlterarSenhaPorEmailForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message=ERRO_INPUT_REQUIRED), Email(message=ERRO_EMAIL), Length(min=1, max=254)])

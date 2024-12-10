from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField('Registrar')

class LoginStep1Form(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    submit = SubmitField('Continuar')

class LoginStep2Form(FlaskForm):
    s = StringField('Prueba (s)', validators=[DataRequired()])
    submit = SubmitField('Verificar')

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, BooleanField, StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = EmailField('Email adress', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators =[DataRequired(), Email()])
    password = PasswordField('Passeword', validators = [DataRequired()])
    hobby = SelectField('Hobby', choices=[('anime', 'Anime'), ('sports', 'Sports'), ('music', 'Music'), ('gaming', 'Gaming')])
    submit = SubmitField('Register')

class MessageForm(FlaskForm):
    message = TextAreaField('Message:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    hobby = StringField('Hobby', validators=[DataRequired()])  # Hobby フィールドを追加
    submit = SubmitField('Update Info')
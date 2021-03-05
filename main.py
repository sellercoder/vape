from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template, redirect
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_wtf.csrf import CsrfProtect
from wtforms.validators import DataRequired
from db import *

app = Flask(__name__)
CsrfProtect(app)
app.config.update(
    DEBUG = True,
    WTF_CSRF_ENABLED = True,
    SECRET_KEY = 'you-will-never-guess',
)

class MyForm(FlaskForm):
	name = StringField('Имя', validators=[DataRequired()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	user = StringField('Юзер')
	service = StringField('Сервис')


@app.route('/', methods=['GET', 'POST'])
def index():
	return Good.all().to_json()
	#return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)






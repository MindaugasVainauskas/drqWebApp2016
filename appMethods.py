#This file will deal with the methods required by the app

from wtforms import Form, BooleanField, StringField, validators, PasswordField

class SignupForm(Form):
	name = StringField('inputName', [validators.Length(min=4, max=20)])
	surname = StringField('inputSurname', [validators.Length(min=4, max=20)])
	password = PasswordField('inputPassword', [
		validators.DataRequired(),
		validators.EqualTo('confirmation', message='Passwords Must Match!')
		])
	confirmation = PasswordField('inputPassConf')
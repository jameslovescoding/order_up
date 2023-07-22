from flask_wtf import FlaskForm

from wtforms.fields import (
    StringField,
    SubmitField,
    PasswordField,
    SelectField
)

from wtforms.validators import (DataRequired, ValidationError)

class LoginForm(FlaskForm):
  employee_number = StringField('Employee number', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Login')

class TableAssignmentForm(FlaskForm):
    tables = SelectField("Tables", coerce=int)
    servers = SelectField("Servers", coerce=int)
    assign = SubmitField("Assign")
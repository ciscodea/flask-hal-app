from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    question = StringField('Pregunta', validators=[DataRequired()])
    submit = SubmitField('Agregar')

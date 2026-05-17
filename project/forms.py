from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class TaskForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField("Описание")
    submit = SubmitField("Сохранить")

class EditTaskForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField("Описание")
    submit = SubmitField("Обновить")
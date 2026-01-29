from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class TaskForm(FlaskForm):
    title = StringField(
        "Task Title",
        validators=[DataRequired(), Length(max=200)]
    )

    description = TextAreaField(
        "Description",
        validators=[Length(max=500)]
    )

    submit = SubmitField("Save Task")

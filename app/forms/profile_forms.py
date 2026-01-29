from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

class ProfileForm(FlaskForm):
    full_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(max=120)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    mobile = StringField(
    "Mobile Number",
    validators=[
        DataRequired(),
        Regexp(r'^[6-9]\d{9}$', message="Enter a valid 10-digit mobile number")
    ]
)


    dob = DateField(
        "Date of Birth",
        validators=[DataRequired()],
        format="%Y-%m-%d"
    )

    gender = SelectField(
        "Gender",
        choices=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other")
        ],
        validators=[DataRequired()]
    )

    occupation = StringField(
        "Occupation",
        validators=[DataRequired(), Length(max=100)]
    )

    submit = SubmitField("Save Profile")

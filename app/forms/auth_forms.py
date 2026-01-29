from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    Regexp,
    ValidationError
)
from app.models.user import User


# -------------------------
# REGISTER FORM
# -------------------------
class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=30)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8),
            Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).+$',
                message="Password must contain uppercase, lowercase, and special character"
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match")
        ]
    )

    submit = SubmitField("Register")
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken. Please choose another.")

# -------------------------
# LOGIN FORM
# -------------------------
class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")


# -------------------------
# FORGOT PASSWORD FORM
# -------------------------
class ForgotPasswordForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    submit = SubmitField("Send OTP")


# -------------------------
# RESET PASSWORD FORM
# -------------------------
class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=8),
            Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).+$',
                message="Password must contain uppercase, lowercase, and special character"
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match")
        ]
    )

    submit = SubmitField("Reset Password")

from flask_wtf import FlaskForm
from flask_wtf.file import file_allowed, FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from BlogApplication.models import User
from flask_login import current_user


class registrationForm(FlaskForm):
    Username = StringField('Username', validators=[DataRequired(), Length(min=2, max=12)])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    Confirmed_password = PasswordField('Confirmed_password', validators=[DataRequired(), EqualTo('Password')])
    Submit = SubmitField('Sign_Up')

    def validate_Username(self, Username):
        use_1 = User.query.filter_by(username=Username.data).first()
        if use_1:
            raise ValidationError("username already exists")

    def validate_Email(self, Email):
        Email_1 = User.query.filter_by(email=Email.data).first()
        if Email_1:
            raise ValidationError("Email already exists")


class LoginForm(FlaskForm):
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    Remember = BooleanField('Remember Me')
    Submit = SubmitField('Login')


class UpdateForm(FlaskForm):
    Username = StringField('Username', validators=[DataRequired(), Length(min=2, max=12)])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Pic', validators=[file_allowed(['jpg', 'png', 'jpeg'])])
    Submit = SubmitField('Update')

    def validate_Username(self, Username):
        if Username.data != current_user.username:
            use_1 = User.query.filter_by(username=Username.data).first()
            if use_1:
                raise ValidationError("username already exists")

    def validate_Email(self, Email):
        if Email.data != current_user.email:
            Email_1 = User.query.filter_by(email=Email.data).first()
            if Email_1:
                raise ValidationError("Email already exists")



class RequestResetForm(FlaskForm):
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Submit = SubmitField('Send Reset Link')

    def validate_Email(self, Email):
            Email_1 = User.query.filter_by(email=Email.data).first()
            if Email_1 is None:
                raise ValidationError("Email Not exists")


class ResetPasswordForm(FlaskForm):
    Password = PasswordField('Password', validators=[DataRequired()])
    Confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Reset Password')
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user




class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)] )
    email = StringField('Email', 
                         validators=[DataRequired(), Email()] )
    password = PasswordField('Password', 
                              validators=[DataRequired()] )
    confirm_password = PasswordField('Confirm Password',
                                      validators=[DataRequired(), EqualTo('password')] )
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Invalid username. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Invalid username. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)] )
    password = PasswordField('Password', 
                              validators=[DataRequired()] )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                         validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture',
                         validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class SalaryInfoForm(FlaskForm):
    hrwkwk = IntegerField('Working Hours(/week)',
                           validators=[DataRequired()] )
    education = SelectField('Education',
                               choices=[(8,'1st-12th'),(9,'HS-grad'),(10.5,'Assoc-acdm/voc'),(12.5,'Some-college/Prof-school'),(14,'Bachelors'),(15,'Masters'),(16,'Doctorate')])
    age = IntegerField('Age',
                        validators=[DataRequired()] )
    submit = SubmitField('Predict')
    


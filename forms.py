from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from wtforms.fields import DateField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class HealthEntryForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], default=lambda: datetime.utcnow().date())
    exercise = StringField('Exercise', validators=[Length(max=200)])
    diet = TextAreaField('Diet', validators=[Length(max=500)])
    mood = SelectField('Mood (1-10)', choices=[(i, str(i)) for i in range(1, 11)], 
                      validators=[NumberRange(min=1, max=10)], coerce=int)
    water_intake = IntegerField('Water Intake (glasses)', validators=[NumberRange(min=0, max=20)])
    sleep_hours = FloatField('Sleep Hours', validators=[NumberRange(min=0, max=24)])
    notes = TextAreaField('Notes')
    submit = SubmitField('Save Entry')
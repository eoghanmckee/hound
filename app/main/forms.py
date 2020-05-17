from flask import request
from flask_wtf import FlaskForm
from app.models import Users, Cases
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CreateAdmin(FlaskForm):

    submit = SubmitField('Create Admin')


class CreateForm(FlaskForm):

    casename = TextAreaField('Case Name [Required]',
                             validators=[DataRequired()])
    slackwebhook = TextAreaField('Slack Webhook')
    names = TextAreaField('Names')
    usernames = TextAreaField('Usernames')
    userids = TextAreaField('UserIDs')
    emails = TextAreaField('Emails')
    phones = TextAreaField('Phones')
    ips = TextAreaField('IPs')
    keywords = TextAreaField('Keywords')
    domains = TextAreaField('Domains')
    urls = TextAreaField('Urls')
    btcaddresses = TextAreaField('BTC Addresses')
    sha256 = TextAreaField('Sha256')
    sha1 = TextAreaField('Sha1')
    md5 = TextAreaField('md5')
    filenames = TextAreaField('Filenames')
    flashpoint = BooleanField('Flashpoint')
    crowdstrike = BooleanField('Crowdstrike')
    postgres = BooleanField('Postgres')

    submit = SubmitField('Submit')

    def validate_casename(self, casename):
        casename = Cases.query.filter_by(casename=casename.data).first()
        if casename is not None:
            raise ValidationError('Please use a different casename.')

class UpdateForm(FlaskForm):

    casename = TextAreaField('Case Name [Required]')
    slackwebhook = TextAreaField('Slack Webhook')
    names = TextAreaField('Names')
    usernames = TextAreaField('Usernames')
    userids = TextAreaField('UserIDs')
    emails = TextAreaField('Emails')
    phones = TextAreaField('Phones')
    ips = TextAreaField('IPs')
    keywords = TextAreaField('Keywords')
    domains = TextAreaField('Domains')
    urls = TextAreaField('Urls')
    btcaddresses = TextAreaField('BTC Addresses')
    sha256 = TextAreaField('Sha256')
    sha1 = TextAreaField('Sha1')
    md5 = TextAreaField('md5')
    filenames = TextAreaField('Filenames')
    flashpoint = BooleanField('Flashpoint')
    crowdstrike = BooleanField('Crowdstrike')
    postgres = BooleanField('Postgres')

    update = SubmitField('Update')
    delete = SubmitField('Delete')
    deactivate = SubmitField('Deactivate')
    activate = SubmitField('Activate')

class NotesForm(FlaskForm):

    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):

    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Submit')
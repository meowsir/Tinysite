from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Password


class LoginForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if(user is not None):
            raise ValidationError('用户名重复')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if(user is not None):
            raise ValidationError('该邮箱已经被注册')


class AddpasswordForm(FlaskForm):
    password_attribute = StringField('属性', validators=[DataRequired()])
    password_account = StringField('账号', validators=[DataRequired()])
    password_body = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('添加')


class EditpasswordForm(FlaskForm):
    password_attribute = StringField('属性', validators=[DataRequired()])
    password_account = StringField('账号', validators=[DataRequired()])
    password_body = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('确认修改')


class PasswordbookForm(FlaskForm):
    search_attribute = StringField("")
    submit = SubmitField('查找')
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Password
from werkzeug.urls import url_parse

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='登录', form=form)


@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='主页')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)


@app.route('/passwordbook', methods=['GET', 'POST'])
@login_required
def passwordbook():
    form = PasswordbookForm()
    if form.validate_on_submit():
        if form.search_attribute.data is "":
            all_passwords = Password.query.filter_by(user_id=current_user.id)
            return render_template('passwordbook.html', my_passwords=all_passwords, form=form)
        else:
            some_passwords = Password.query.filter_by(
                password_attribute=form.search_attribute.data, user_id=current_user.id)
            if some_passwords.count() == 0:
                flash("未找到密码")
                all_passwords = Password.query.filter_by(user_id=current_user.id)
                return render_template('passwordbook.html', my_passwords=all_passwords, form=form)
            flash("查找到密码")
            return render_template('passwordbook.html', my_passwords=some_passwords, form=form)
    my_passwords = Password.query.filter_by(user_id=current_user.id)
    return render_template('passwordbook.html', my_passwords=my_passwords, form=form)


@app.route('/addpassword', methods=['GET', 'POST'])
@login_required
def addpassword():
    form = AddpasswordForm()
    if form.validate_on_submit():
        password = Password(password_attribute=form.password_attribute.data,
                            password_account=form.password_account.data, password_body=form.password_body.data, user_id=current_user.id)
        db.session.add(password)
        db.session.commit()
        flash('添加密码成功')
        return redirect(url_for('passwordbook'))
    return render_template('addpassword.html', title='添加新的密码', form=form)


@app.route('/editpassword/<int:password_id>', methods=['GET', 'POST'])
@login_required
def editpassword(password_id):
    form = EditpasswordForm()
    if form.validate_on_submit():
        password = Password.query.get(password_id)
        if request.method == 'POST':
            password.password_attribute = request.form['password_attribute']
            password.password_account = request.form['password_account']
            password.password_body = request.form['password_body']
        db.session.commit()
        flash('修改成功')
        return redirect(url_for('passwordbook'))
    return render_template('editpassword.html', title='修改密码', form=form)


@app.route('/deletepassword/<int:password_id>', methods=['GET', 'POST'])
@login_required
def deletepassword(password_id):
    password = Password.query.get(password_id)
    db.session.delete(password)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('passwordbook'))

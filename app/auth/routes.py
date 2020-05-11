from app.auth import bp
from config import Config
from app.models import Users
from app import db, create_app
from werkzeug.urls import url_parse
from slackmessenger import Slackmessenger
from flask_login import login_user, logout_user, current_user
from flask import render_template, redirect, url_for, request, flash
from app.auth.forms import LoginForm, RegistrationForm, CreateAdmin, EditUser
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():

    @bp.route('/login', methods=['GET', 'POST'])
    def login(config_class=Config):

        form = LoginForm()
        admin_username = app.config['CONFIG']['admin_username']
        
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):

                return redirect(url_for('auth.login'))

            login_user(user, remember=form.remember_me.data)

            if current_user.username == admin_username:
                return redirect(url_for('auth.users'))

            next_page = request.args.get('next')

            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')

            return redirect(next_page)

        return render_template('auth/login.html', title='Sign In', form=form)


    @bp.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('main.index'))


    @bp.route('/register', methods=['GET', 'POST'])
    def register(config_class=Config):

        admin_username = app.config['CONFIG']['admin_username']

        if current_user.username == admin_username:
            form = RegistrationForm()
            if form.validate_on_submit():
                user = Users(username=form.username.data,
                            email=form.email.data)
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                
                Slackmessenger().accountcreated(form.username.data, form.email.data)

                flashmessage = \
                    'Account created for: {}'.format(form.username.data)
                flash(flashmessage)
                return redirect(url_for('auth.users'))
        return render_template('auth/register.html', title='Register',
                               form=form)


    @bp.route('/createadmin', methods=['GET', 'POST'])
    def createadmin(config_class=Config):
        
        form = CreateAdmin()

        admin_username = app.config['CONFIG']['admin_username']
        admin = Users.query.filter_by(username=admin_username).all()

        if form.validate_on_submit():
            if not admin:
                admin_email = app.config['CONFIG']['admin_email']
                admin_password = app.config['CONFIG']['admin_password']

                u = Users(username=admin_username, email=admin_email)
                u.set_password(admin_password)
                db.session.add(u)
                db.session.commit()

                Slackmessenger().accountcreated(admin_username, admin_email)

                flash('Account created for admin')
                return redirect(url_for('auth.login'))
            flash('Admin account already created')
            return redirect(url_for('main.index'))

        return render_template('auth/createadmin.html', title='Create', form=form)


    @bp.route('/users')
    def users(config_class=Config):
        admin_username = app.config['CONFIG']['admin_username']

        if current_user.username != admin_username:
            return render_template('index.html', title='Home')

        users = Users.query.all()
        return render_template('auth/users.html', title='Users', users=users)


    @bp.route('/edituser/<id>', methods=['GET', 'POST'])
    def edituser(id):
        user = Users.query.filter_by(id=id).first()
        form = EditUser()
        admin_username = app.config['CONFIG']['admin_username']

        if current_user.username != admin_username:
            return render_template('index.html', title='Home')

        if current_user.username == admin_username:

            if request.method == 'GET':
                # prepopulate the form with existing iocs
                form.username.data=user.username
                form.email.data=user.email
            
            # if updating User:
            if form.update.data:

                if form.username.data:
                    update = Users.query.filter_by(id=id).first()
                    update.username = form.username.data
                    db.session.commit()

                if form.email.data:
                    update = Users.query.filter_by(id=id).first()
                    update.email = form.email.data
                    db.session.commit()

                if form.password.data:
                    update = Users.query.filter_by(id=id).first()
                    new_pass = form.password.data
                    pass_hash = generate_password_hash(new_pass)
                    update.password_hash = pass_hash
                    db.session.add(update)
                    db.session.commit()

                flash('Account updated')

                return redirect(url_for('auth.users'))

            # if deleting user
            if form.delete.data:

                flashmessage = \
                'User "{}" deleted'.format(user.username)

                Users.query.filter_by(id=id).delete()
                db.session.commit()
                flash(flashmessage)
                return redirect(url_for('auth.users'))


        return render_template(
            'auth/edituser.html',
            title='Edit User',
            user=user,
            form=form
            )
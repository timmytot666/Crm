from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from users.models import User, Role # Corrected import path
from users.forms import LoginForm, RegistrationForm # Corrected import path

users_bp = Blueprint('users', __name__, template_folder='../templates/users') # Specific template folder

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.index')) # Or a dashboard route
    form = RegistrationForm()
    if form.validate_on_submit():
        # Assign Sales User role by default for new registrations
        sales_user_role = Role.query.filter_by(name='Sales User').first()
        if not sales_user_role:
            # This is a fallback, roles should be pre-populated
            flash('Default user role not found. Please contact admin.', 'danger')
            return redirect(url_for('users.register'))
        user = User(username=form.username.data, email=form.email.data, role=sales_user_role)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.index')) # Or a dashboard route
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('users.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('users.index')) # Or a dashboard route
    return render_template('login.html', title='Sign In', form=form)

@users_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users_bp.route('/') # Basic index/profile placeholder
@login_required
def index():
    return render_template('user_profile.html', title='Profile')

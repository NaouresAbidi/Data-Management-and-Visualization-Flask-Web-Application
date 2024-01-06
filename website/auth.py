from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User
from flask_login import login_user, logout_user, login_required
from app import db

auth = Blueprint('auth', __name__)
app = Blueprint('app', __name__)


@auth.route('/logout', methods=['GET', 'POST',])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        username = request.form.get('username')
        password2 = request.form.get('password2')
        select_field = request.form.get('select_field')
        telephone = request.form.get('telephone')
        birthdate = request.form.get('birthdate')
        birthplace = request.form.get('birthplace')
        nationality = request.form.get('nationality')
        cin = request.form.get('cin')
        address = request.form.get('address')
        password = request.form.get('password1')

        if len(firstName) < 2:
            flash('First name must have more than 2 characters.',
                  category="Error")
            return redirect(url_for('auth.sign_up'))
        elif len(lastName) < 2:
            flash('Last name must have more than 2 characters.',
                  category='Error')
            return redirect(url_for('auth.sign_up'))
        elif not select_field:
            flash('Team is required.', category='Error')
            return redirect(url_for('auth.sign_up'))
        elif len(email) < 4:
            flash('Email must have more than 4 characters.', category='Error')
            return redirect(url_for('auth.sign_up'))
        elif len(birthdate) < 7:
            flash('Birthdate is not complete', category='Error')
            return redirect(url_for('auth.sign_up'))
        elif len(birthplace) < 1:
            flash('Birthplace is not complete', category='Error')
            return redirect(url_for('auth.sign_up'))
        elif len(str(telephone)) != 8:
            flash(
                'Phone number cannot contain more or less than 8 number', category='Error')
            return redirect(url_for('auth.sign_up'))
        elif len(nationality) < 2:
            flash('Please provide the nationality', category='Error')
            return redirect(url_for('auth.sign_up'))
        elif not cin:
            flash('Please provide a CIN number or your passport number',
                  category='Error')
            return redirect(url_for('auth.sign_up'))
        elif not address:
            flash('Please provide the full address', category='Error')
            return redirect(url_for('auth.sign_up'))
        elif not email or not password:
            flash('Username and password are required', category='Error')
            return redirect(url_for('auth.sign_up'))
        elif password != password2:
            flash('Passwords do not match.', category='Error')
            return redirect(url_for('auth.sign_up'))
        elif User.query.filter_by(email=email).first():
            flash('This email is associated to another user', category='Error')
            return redirect(url_for('auth.sign_up'))
        elif User.query.filter_by(username=username).first():
            flash('This username is associated to another user', category='Error')
            return redirect(url_for('auth.sign_up'))
        else:
            user = User(email, password, firstName, lastName, select_field, telephone,
                        birthplace, birthdate, nationality, address, cin, username, password2)
            db.session.add(user)
            db.session.commit()
            flash('Account created!', category='Success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html")


@auth.route('/login', methods=['GET', 'POST',])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Please verify your email or password', category='Error')
            return redirect(url_for('auth.login'))

        login_user(user, remember=True)
        return redirect(url_for('views.dashboard'))

    return render_template('login.html')

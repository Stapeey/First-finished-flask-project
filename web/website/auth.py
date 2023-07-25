from flask import Blueprint, render_template, flash, request, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

logged = False

auth = Blueprint('auth', __name__) 
from . import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    global logged
    global current_user
    if logged:
        flash('Already logged in!', category='error')
        return redirect(url_for('views.home')+ '#latest')
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            EmailPW = db.session.execute(db.select(User).where(User.email == email)).all()
            if EmailPW != []:
                EmailPW = EmailPW[0][0]
                if check_password_hash(EmailPW.password, password):
                    current_user = EmailPW.id
                    flash(f'Successfully logged in! Welcome {EmailPW.first_name}!', category='success')
                    logged = True
                    return redirect(url_for('views.home')+ '#latest')
                else:
                    flash('Wrong email and password combination.', category='error')
                    return render_template("login.html")
            else:
                flash('Wrong email and password combination.', category='error')
                return render_template("login.html")
        else:
            return render_template("login.html")
            
    
@auth.route('/logout')
def logout():
    global logged
    global finalload
    global current_user
    if logged:
        flash('Logged out successfully!', category='success')
        finalload = []
        current_user = None
        logged = False
        return redirect(url_for('views.home'))
    else:
        flash('You are not logged in!', category='error')
        return redirect(url_for('views.home'))
    

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print(email, first_name, password1, password2)

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        else:
            result = bool(User.query.filter_by(email=email).count())
            if result:
                flash('Email has already been used.', category='error')
            else:
                if len(first_name) <2:
                    flash('First name must be greater than 2 characters.', category='error')
                elif password1 != password2:
                    flash("Passwords don't match", category='error')
                elif len(password1) < 7:
                    flash('Password must be at least 7 characters', category='error')
                else:
                    new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Account created!', category='success')
                    return redirect(url_for('views.home'))

    return render_template("sign_up.html")
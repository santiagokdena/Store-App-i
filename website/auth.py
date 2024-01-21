from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
auth = Blueprint('auth', __name__)
@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        user=User.objects(user=username).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                flash('Ha iniciado sesion satisfactoriamente',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.orders'))
            else:
                flash('Contraseña incorrecta, intente de nuevo',category='error')
        else:
            flash('El usuario no existe, intente de nuevo', category='error')
    return render_template("login.html",user=current_user)
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('user')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user=User.objects(user=username).first()
        if user:
            flash('Esta cuenta ya existe!', category='error')
        elif password1!=password2:
            flash('Las contraseñas no son iguales', category='error')
        else:
            new_user = User(user=username,password=bcrypt.generate_password_hash(password1).decode('utf-8'))
            new_user.save()
            login_user(new_user, remember=True)
            flash('Cuenta creada!', category='success')
            return redirect(url_for('views.orders'))
    return render_template("sign-up.html", user=current_user)

#super USERurl_for('static', filename='style.css')
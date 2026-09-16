from flask import request, redirect, url_for, render_template, Blueprint, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from crm_system import db, login_manager
from crm_system.models.user import User
from flask_login import logout_user

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template('main.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('views.home'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@views.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        age = request.form.get('age')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('views.register'))

        if len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
            return redirect(url_for('views.register'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'error')
            return redirect(url_for('views.register'))

        try:
            age = int(age)
            if age < 16:
                flash('You must be at least 16 years old to register', 'error')
                return redirect(url_for('views.register'))
        except ValueError:
            flash('Please enter a valid age', 'error')
            return redirect(url_for('views.register'))

        new_user = User(
            name=name,
            surname=surname,
            age=age,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('views.login'))

    return render_template('register.html')

@views.route('/flower')
def flower():
    return render_template('flower.html')

@views.route('/gift')
def gift():
    return render_template('gift.html')

@views.route('/funeral')
def funeral():
    return render_template('funeral.html')

@views.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')

@views.route('/mother')
def mother():
    return render_template('mother.html')

@views.route('/occasion')
def occasion():
    return render_template('occasion.html')

@views.route('/password')
def password():
    return render_template('password.html')

@views.route('/order')
def order():
    return render_template('order.html')

@views.route("/user_management", methods=["GET", "POST"])
@login_required
def user_management():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        age = request.form["age"]
        email = request.form["email"]
        password = request.form["password"]
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'error')
            return redirect(url_for('views.user_management'))

        user = User(
            name=name,
            surname=surname,
            age=age,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('views.user_management'))

    users = User.query.all()
    return render_template("user_management.html", users=users)

@views.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('You cannot delete your own account!', 'error')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    return redirect(url_for('views.user_management'))

@views.route("/logout", methods=['POST'])
@login_required 
def logout():
    logout_user() 
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('views.login'))
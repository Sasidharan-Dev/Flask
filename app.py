import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
import click

# ----------------------
# App configuration
# ----------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# ----------------------
# Database model
# ----------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ----------------------
# Auto DB initialization
# ----------------------
def init_db_if_needed():
    """Auto-initialize DB if it doesn't exist yet."""
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace("sqlite:///", "")
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            print("✅ Database initialized automatically (first run).")


init_db_if_needed()


# ----------------------
# CLI command (manual init)
# ----------------------
@app.cli.command("init-db")
def init_db():
    """Initialize the database manually."""
    with app.app_context():
        db.create_all()
        click.echo("✅ Database initialized!")


# ----------------------
# Routes
# ----------------------
@app.route('/')
@login_required
def index():
    users = User.query.all()
    return render_template('list_users.html', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/register-admin', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        if password != password2:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register_admin'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'danger')
            return redirect(url_for('register_admin'))

        new_admin = User(name=name, email=email, is_admin=True)
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()
        flash('New admin registered successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register_admin.html')


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        if password != password2:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('add_user'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'danger')
            return redirect(url_for('add_user'))

        new_user = User(name=name, email=email, is_admin=False)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_user.html')


@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        if password or password2:
            if password != password2:
                flash('Passwords do not match!', 'danger')
                return redirect(url_for('edit_user', user_id=user.id))
            user.set_password(password)

        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_user.html', user=user)


@app.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'info')
    return redirect(url_for('index'))


# ----------------------
# Run app
# ----------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

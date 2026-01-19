#!/usr/bin/env python3

from flask import Flask, render_template, flash, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from typing import Any, Literal


class User(UserMixin):
    def __init__(self, id: int, username: str, email: str, password: str):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    @property
    def is_authenticated(self) -> Literal[True]:
        """Return True as the user is authenticated."""
        return True

    @property
    def is_active(self) -> Literal[True]:
        """Return True as the user account is active."""
        return True

    @property
    def is_anonymous(self) -> Literal[False]:
        """Return False as anonymous users aren't supported."""
        return False

    def get_id(self) -> str:
        """Return the user ID as a string."""
        return str(self.id)

    def __repr__(self) -> str:
        return f'<User {self.username}>'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'  # TODO: Change this to a secure secret key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # type: ignore

# Temporary user storage (replace with database in production)
users = {
    1: User(id=1, username='testuser', email='test@example.com', password='password123')
}


@login_manager.user_loader
def load_user(user_id: str) -> Any:
    """Load user by ID from session."""
    return users.get(int(user_id))


@app.route("/")
def index() -> Any:
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login() -> Any:
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Find user by username (in production, use database)
        user = next((u for u in users.values() if u.username == username), None)
        
        if user and user.password == password:
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout() -> Any:
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
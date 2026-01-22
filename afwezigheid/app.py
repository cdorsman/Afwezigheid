#!/usr/bin/env python3

from os import getenv
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import generate_csrf
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Any, Optional

from models import db, User, Aanwezigheid

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY', 'your-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}"
    f"@{getenv('DB_HOST', 'localhost')}:{getenv('DB_PORT', 3306)}/{getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['WTF_CSRF_ENABLED'] = getenv('FLASK_ENV') != 'development'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.context_processor
def inject_csrf_token():
    """Inject CSRF token into all templates."""
    return dict(csrf_token=generate_csrf)


@login_manager.user_loader
def load_user(werknemer_id: str) -> Optional[User]:
    """Load user by ID from database."""
    return User.query.get(int(werknemer_id))


@app.route("/", methods=['GET', 'POST'])
@login_required
def index() -> Any:
    if request.method == 'POST':
        action = request.form.get('action')
        
        # Acties voor normale werknemers
        if current_user.rol != 'teamleider':
            if action == 'create':
                try:
                    check_in = datetime.fromisoformat(request.form.get('check_in'))
                    check_uit_str = request.form.get('check_uit')
                    check_uit = datetime.fromisoformat(check_uit_str) if check_uit_str else None
                    status = request.form.get('status')
                    notities = request.form.get('notities')
                    
                    nieuwe_record = Aanwezigheid(
                        werknemer_id=current_user.werknemer_id,
                        check_in=check_in,
                        check_uit=check_uit,
                        status=status,
                        notities=notities,
                        goedkeuring_status='pending'
                    )
                    
                    db.session.add(nieuwe_record)
                    db.session.commit()
                except Exception as e:
                    print(f"Error creating record: {e}")
                return redirect(url_for('index'))
            
            elif action == 'delete':
                try:
                    record_id = int(request.form.get('record_id'))
                    record = Aanwezigheid.query.get(record_id)
                    
                    if record and record.werknemer_id == current_user.werknemer_id:
                        db.session.delete(record)
                        db.session.commit()
                except Exception as e:
                    print(f"Error deleting record: {e}")
                return redirect(url_for('index'))
        
        # Acties voor teamleiders
        elif current_user.rol == 'teamleider':
            if action == 'approve':
                try:
                    record_id = int(request.form.get('record_id'))
                    record = Aanwezigheid.query.get(record_id)
                    
                    if record:
                        record.goedkeuring_status = 'approved'
                        db.session.commit()
                except Exception as e:
                    print(f"Error approving record: {e}")
                return redirect(url_for('index'))
            
            elif action == 'reject':
                try:
                    record_id = int(request.form.get('record_id'))
                    record = Aanwezigheid.query.get(record_id)
                    
                    if record:
                        record.goedkeuring_status = 'rejected'
                        db.session.commit()
                except Exception as e:
                    print(f"Error rejecting record: {e}")
                return redirect(url_for('index'))
    
    # Data laden op basis van rol
    if current_user.rol == 'teamleider':
        aanwezigheid_records = Aanwezigheid.query.filter_by(goedkeuring_status='pending').all()
    else:
        aanwezigheid_records = Aanwezigheid.query.filter_by(
            werknemer_id=current_user.werknemer_id
        ).all()

    return render_template( 
        'index.html',
        aanwezigheid=aanwezigheid_records,
        user=current_user,
        rol=current_user.rol
    )


@app.route('/login', methods=['GET', 'POST'])
def login() -> Any:
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        gebruikersnaam = request.form.get('username')
        wachtwoord = request.form.get('password')
        
        gebruiker = User.query.filter_by(gebruikersnaam=gebruikersnaam).first()
        
        if gebruiker and gebruiker.verify_password(wachtwoord):
            login_user(gebruiker, remember=True)
            return redirect(url_for('index'))
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout() -> Any:
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
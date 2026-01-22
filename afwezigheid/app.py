#!/usr/bin/env python3

from os import getenv
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import generate_csrf
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
from typing import Any, Optional

from models import db, User, Verlof

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
    """Manage leave requests."""
    if request.method == 'POST':
        action = request.form.get('action')
        
        # Werknemers: verlofaanvraag indienen
        if current_user.rol != 'teamleider':
            if action == 'request':
                try:
                    verlof_type = request.form.get('verlof_type')
                    start_datum = datetime.strptime(request.form.get('start_datum'), '%Y-%m-%d').date()
                    eind_datum = datetime.strptime(request.form.get('eind_datum'), '%Y-%m-%d').date()
                    
                    nieuw_verlof = Verlof(
                        werknemer_id=current_user.werknemer_id,
                        verlof_type=verlof_type,
                        start_datum=start_datum,
                        eind_datum=eind_datum,
                        status='In behandeling'
                    )
                    
                    db.session.add(nieuw_verlof)
                    db.session.commit()
                except Exception as e:
                    print(f"Error creating leave request: {e}")
                return redirect(url_for('index'))
            
            elif action == 'delete':
                try:
                    verlof_id = int(request.form.get('verlof_id'))
                    verlof_record = Verlof.query.get(verlof_id)
                    
                    if verlof_record and verlof_record.werknemer_id == current_user.werknemer_id:
                        db.session.delete(verlof_record)
                        db.session.commit()
                except Exception as e:
                    print(f"Error deleting leave request: {e}")
                return redirect(url_for('index'))
        
        # Teamleiders: verlofaanvraag goedkeuren/afkeuren
        elif current_user.rol == 'teamleider':
            if action == 'approve':
                try:
                    verlof_id = int(request.form.get('verlof_id'))
                    verlof_record = Verlof.query.get(verlof_id)
                    
                    if verlof_record:
                        verlof_record.status = 'Goedgekeurd'
                        verlof_record.goedgekeurd_door = current_user.werknemer_id
                        db.session.commit()
                except Exception as e:
                    print(f"Error approving leave: {e}")
                return redirect(url_for('index'))
            
            elif action == 'reject':
                try:
                    verlof_id = int(request.form.get('verlof_id'))
                    verlof_record = Verlof.query.get(verlof_id)
                    
                    if verlof_record:
                        verlof_record.status = 'Afgekeurd'
                        verlof_record.goedgekeurd_door = current_user.werknemer_id
                        db.session.commit()
                except Exception as e:
                    print(f"Error rejecting leave: {e}")
                return redirect(url_for('index'))
    
    # Data laden op basis van rol
    if current_user.rol == 'teamleider':
        verlof_records = Verlof.query.filter_by(status='In behandeling').all()
    else:
        verlof_records = Verlof.query.filter_by(
            werknemer_id=current_user.werknemer_id
        ).all()
    
    return render_template(
        'index.html',
        verlof=verlof_records,
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
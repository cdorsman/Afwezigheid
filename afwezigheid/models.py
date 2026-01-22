from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from hashlib import sha512

db = SQLAlchemy()

class UserSchema(BaseModel):
    """Pydantic schema for user validation."""
    werknemer_id: int
    gebruikersnaam: str
    wachtwoord_hash: str
    rol: str
    
    @field_validator('gebruikersnaam')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        assert v.isalnum(), 'Gebruikersnaam moet alphanumeriek zijn'
        return v

class User(UserMixin, db.Model):
    """User model for database."""
    __tablename__ = 'Gebruikers'
    
    werknemer_id = db.Column(db.Integer, primary_key=True)
    gebruikersnaam = db.Column(db.String(80), unique=True, nullable=False)
    wachtwoord_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return f'<User {self.gebruikersnaam}>'
    
    def get_id(self) -> str:
        """Return the user ID as a string for Flask-Login."""
        return str(self.werknemer_id)
    
    def verify_password(self, wachtwoord: str) -> bool:
        """Verify password using SHA512 hash."""
        wachtwoord_hash = sha512(wachtwoord.encode()).hexdigest()
        return self.wachtwoord_hash == wachtwoord_hash
    
    def to_schema(self) -> UserSchema:
        """Convert to Pydantic schema."""
        return UserSchema(
            werknemer_id=self.werknemer_id,
            gebruikersnaam=self.gebruikersnaam,
            wachtwoord_hash=self.wachtwoord_hash,
            rol=self.rol
        )


class AanwezigheidSchema(BaseModel):
    """Pydantic schema for attendance validation."""
    aanwezigheid_id: int
    werknemer_id: int
    check_in: datetime
    check_uit: Optional[datetime] = None
    status: str
    notities: Optional[str] = None
    
    @field_validator('status')
    @classmethod
    def status_valid(cls, v: str) -> str:
        valid_statuses = ['Aanwezig', 'Afwezig', 'Ziek', 'Verlof']
        assert v in valid_statuses, f'Status moet een van deze zijn: {valid_statuses}'
        return v


class Aanwezigheid(db.Model):
    """Attendance record model for database."""
    __tablename__ = 'Aanwezigheid'
    
    aanwezigheid_id = db.Column(db.Integer, primary_key=True)
    werknemer_id = db.Column(db.Integer, db.ForeignKey('Gebruikers.werknemer_id'), nullable=False)
    check_in = db.Column(db.DateTime, nullable=False)
    check_uit = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(255), nullable=False)
    notities = db.Column(db.String(255), nullable=True)
    goedkeuring_status = db.Column(db.String(20), nullable=False, default='pending')
    
    def __repr__(self) -> str:
        return f'<Aanwezigheid {self.werknemer_id} - {self.check_in}>'
    
    def to_schema(self) -> AanwezigheidSchema:
        """Convert to Pydantic schema."""
        return AanwezigheidSchema(
            aanwezigheid_id=self.aanwezigheid_id,
            werknemer_id=self.werknemer_id,
            check_in=self.check_in,
            check_uit=self.check_uit,
            status=self.status,
            notities=self.notities
        )
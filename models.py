from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """PVEDI users who can associate themselves for relationship tracking"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    notes = db.relationship('Note', backref='author', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Firm(db.Model):
    """Companies/organizations in the CRM"""
    __tablename__ = 'firms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    industry = db.Column(db.String(100))
    website = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    contacts = db.relationship('Contact', backref='firm', lazy=True, cascade='all, delete-orphan')
    projects = db.relationship('Project', backref='firm', lazy=True, cascade='all, delete-orphan')
    notes = db.relationship('Note', backref='firm', lazy=True, foreign_keys='Note.firm_id', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Firm {self.name}>'


class Contact(db.Model):
    """Individual contacts belonging to firms"""
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    position = db.Column(db.String(100))
    firm_id = db.Column(db.Integer, db.ForeignKey('firms.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    notes = db.relationship('Note', backref='contact', lazy=True, foreign_keys='Note.contact_id', cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<Contact {self.full_name}>'


# Association table for many-to-many relationship between projects and contacts
project_contacts = db.Table('project_contacts',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('contact_id', db.Integer, db.ForeignKey('contacts.id'), primary_key=True)
)


class Project(db.Model):
    """Projects linked to firms and contacts"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='Active')  # Active, Completed, On Hold, Cancelled
    firm_id = db.Column(db.Integer, db.ForeignKey('firms.id'), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    contacts = db.relationship('Contact', secondary=project_contacts, backref='projects')
    notes = db.relationship('Note', backref='project', lazy=True, foreign_keys='Note.project_id', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Project {self.name}>'


class Note(db.Model):
    """Timestamped notes with user attribution for all entities"""
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys for different entity types (only one should be set)
    firm_id = db.Column(db.Integer, db.ForeignKey('firms.id'), nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    
    def __repr__(self):
        return f'<Note {self.id} by User {self.user_id}>'
    
    @property
    def entity_type(self):
        if self.firm_id:
            return 'Firm'
        elif self.contact_id:
            return 'Contact'
        elif self.project_id:
            return 'Project'
        return 'Unknown'
    
    @property
    def entity(self):
        if self.firm_id:
            return self.firm
        elif self.contact_id:
            return self.contact
        elif self.project_id:
            return self.project
        return None

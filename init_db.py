"""
Database initialization and sample data seeding script
"""
from app import app, db
from models import User, Firm, Contact, Project, Note
from datetime import datetime, timedelta


def init_db():
    """Initialize the database and create tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")


def seed_sample_data():
    """Add sample data to the database"""
    with app.app_context():
        # Check if data already exists
        if User.query.first():
            print("Database already contains data. Skipping seed.")
            return
        
        # Create users
        admin = User(username='admin', email='admin@pvedi.com')
        john = User(username='john', email='john@pvedi.com')
        db.session.add_all([admin, john])
        db.session.commit()
        print("Created users")
        
        # Create firms
        firm1 = Firm(
            name='Tech Innovations Inc.',
            industry='Technology',
            website='https://techinnovations.example.com',
            phone='+1-555-0101',
            address='123 Silicon Valley, CA 94025'
        )
        
        firm2 = Firm(
            name='Global Consulting Group',
            industry='Consulting',
            website='https://globalconsulting.example.com',
            phone='+1-555-0202',
            address='456 Wall Street, NY 10005'
        )
        
        firm3 = Firm(
            name='Green Energy Solutions',
            industry='Energy',
            website='https://greenenergy.example.com',
            phone='+1-555-0303',
            address='789 Renewable Ave, Austin, TX 78701'
        )
        
        db.session.add_all([firm1, firm2, firm3])
        db.session.commit()
        print("Created firms")
        
        # Create contacts
        contact1 = Contact(
            first_name='Alice',
            last_name='Johnson',
            email='alice.johnson@techinnovations.example.com',
            phone='+1-555-1001',
            position='CTO',
            firm_id=firm1.id
        )
        
        contact2 = Contact(
            first_name='Bob',
            last_name='Smith',
            email='bob.smith@techinnovations.example.com',
            phone='+1-555-1002',
            position='Product Manager',
            firm_id=firm1.id
        )
        
        contact3 = Contact(
            first_name='Carol',
            last_name='Davis',
            email='carol.davis@globalconsulting.example.com',
            phone='+1-555-2001',
            position='Senior Partner',
            firm_id=firm2.id
        )
        
        contact4 = Contact(
            first_name='David',
            last_name='Wilson',
            email='david.wilson@greenenergy.example.com',
            phone='+1-555-3001',
            position='CEO',
            firm_id=firm3.id
        )
        
        db.session.add_all([contact1, contact2, contact3, contact4])
        db.session.commit()
        print("Created contacts")
        
        # Create projects
        project1 = Project(
            name='Mobile App Development',
            description='Developing a new mobile application for iOS and Android',
            status='Active',
            firm_id=firm1.id,
            start_date=(datetime.now() - timedelta(days=30)).date(),
            end_date=(datetime.now() + timedelta(days=90)).date()
        )
        project1.contacts.extend([contact1, contact2])
        
        project2 = Project(
            name='Digital Transformation',
            description='Complete digital transformation strategy and implementation',
            status='Active',
            firm_id=firm2.id,
            start_date=(datetime.now() - timedelta(days=60)).date(),
            end_date=(datetime.now() + timedelta(days=180)).date()
        )
        project2.contacts.append(contact3)
        
        project3 = Project(
            name='Solar Panel Installation',
            description='Installation of solar panels for commercial building',
            status='Completed',
            firm_id=firm3.id,
            start_date=(datetime.now() - timedelta(days=90)).date(),
            end_date=(datetime.now() - timedelta(days=10)).date()
        )
        project3.contacts.append(contact4)
        
        db.session.add_all([project1, project2, project3])
        db.session.commit()
        print("Created projects")
        
        # Create notes
        note1 = Note(
            content='Initial meeting went well. They are interested in our proposal.',
            user_id=admin.id,
            firm_id=firm1.id,
            created_at=datetime.now() - timedelta(days=5)
        )
        
        note2 = Note(
            content='Discussed project timeline and deliverables.',
            user_id=john.id,
            project_id=project1.id,
            created_at=datetime.now() - timedelta(days=3)
        )
        
        note3 = Note(
            content='Follow-up call scheduled for next week.',
            user_id=admin.id,
            contact_id=contact1.id,
            created_at=datetime.now() - timedelta(days=2)
        )
        
        note4 = Note(
            content='Contract signed. Project kickoff meeting scheduled.',
            user_id=admin.id,
            firm_id=firm2.id,
            created_at=datetime.now() - timedelta(days=1)
        )
        
        note5 = Note(
            content='Project completed successfully. Client very satisfied.',
            user_id=john.id,
            project_id=project3.id,
            created_at=datetime.now() - timedelta(hours=12)
        )
        
        db.session.add_all([note1, note2, note3, note4, note5])
        db.session.commit()
        print("Created notes")
        
        print("\nSample data seeded successfully!")
        print(f"Created {User.query.count()} users")
        print(f"Created {Firm.query.count()} firms")
        print(f"Created {Contact.query.count()} contacts")
        print(f"Created {Project.query.count()} projects")
        print(f"Created {Note.query.count()} notes")


if __name__ == '__main__':
    init_db()
    seed_sample_data()

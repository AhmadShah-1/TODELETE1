import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Firm, Contact, Project, Note
from sqlalchemy import or_, desc

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///minicrm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def index():
    """Homepage with global search, add-firm action, and filterable recent activity feed"""
    search_query = request.args.get('search', '')
    activity_filter = request.args.get('filter', 'all')
    
    # Global search across all entities
    firms = []
    contacts = []
    projects = []
    
    if search_query:
        firms = Firm.query.filter(
            or_(
                Firm.name.ilike(f'%{search_query}%'),
                Firm.industry.ilike(f'%{search_query}%')
            )
        ).all()
        
        contacts = Contact.query.filter(
            or_(
                Contact.first_name.ilike(f'%{search_query}%'),
                Contact.last_name.ilike(f'%{search_query}%'),
                Contact.email.ilike(f'%{search_query}%')
            )
        ).all()
        
        projects = Project.query.filter(
            or_(
                Project.name.ilike(f'%{search_query}%'),
                Project.description.ilike(f'%{search_query}%')
            )
        ).all()
    
    # Recent activity feed - get recent notes with filtering
    notes_query = Note.query
    
    if activity_filter != 'all':
        if activity_filter == 'firms':
            notes_query = notes_query.filter(Note.firm_id.isnot(None))
        elif activity_filter == 'contacts':
            notes_query = notes_query.filter(Note.contact_id.isnot(None))
        elif activity_filter == 'projects':
            notes_query = notes_query.filter(Note.project_id.isnot(None))
    
    recent_notes = notes_query.order_by(desc(Note.created_at)).limit(20).all()
    
    # Get recent firms for quick access
    recent_firms = Firm.query.order_by(desc(Firm.created_at)).limit(5).all()
    
    return render_template('index.html',
                         search_query=search_query,
                         firms=firms,
                         contacts=contacts,
                         projects=projects,
                         recent_notes=recent_notes,
                         recent_firms=recent_firms,
                         activity_filter=activity_filter)


@app.route('/firms')
def firms_list():
    """List all firms"""
    firms = Firm.query.order_by(Firm.name).all()
    return render_template('firms_list.html', firms=firms)


@app.route('/firm/<int:firm_id>')
def firm_detail(firm_id):
    """Firm detail page"""
    firm = Firm.query.get_or_404(firm_id)
    notes = Note.query.filter_by(firm_id=firm_id).order_by(desc(Note.created_at)).all()
    return render_template('firm_detail.html', firm=firm, notes=notes)


@app.route('/firm/add', methods=['GET', 'POST'])
def firm_add():
    """Add new firm"""
    if request.method == 'POST':
        firm = Firm(
            name=request.form['name'],
            industry=request.form.get('industry'),
            website=request.form.get('website'),
            phone=request.form.get('phone'),
            address=request.form.get('address')
        )
        db.session.add(firm)
        db.session.commit()
        flash(f'Firm "{firm.name}" created successfully!', 'success')
        return redirect(url_for('firm_detail', firm_id=firm.id))
    
    return render_template('firm_form.html')


@app.route('/firm/<int:firm_id>/edit', methods=['GET', 'POST'])
def firm_edit(firm_id):
    """Edit existing firm"""
    firm = Firm.query.get_or_404(firm_id)
    
    if request.method == 'POST':
        firm.name = request.form['name']
        firm.industry = request.form.get('industry')
        firm.website = request.form.get('website')
        firm.phone = request.form.get('phone')
        firm.address = request.form.get('address')
        db.session.commit()
        flash(f'Firm "{firm.name}" updated successfully!', 'success')
        return redirect(url_for('firm_detail', firm_id=firm.id))
    
    return render_template('firm_form.html', firm=firm)


@app.route('/contact/<int:contact_id>')
def contact_detail(contact_id):
    """Contact detail page"""
    contact = Contact.query.get_or_404(contact_id)
    notes = Note.query.filter_by(contact_id=contact_id).order_by(desc(Note.created_at)).all()
    return render_template('contact_detail.html', contact=contact, notes=notes)


@app.route('/contact/add/<int:firm_id>', methods=['GET', 'POST'])
def contact_add(firm_id):
    """Add new contact to a firm"""
    firm = Firm.query.get_or_404(firm_id)
    
    if request.method == 'POST':
        contact = Contact(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            position=request.form.get('position'),
            firm_id=firm_id
        )
        db.session.add(contact)
        db.session.commit()
        flash(f'Contact "{contact.full_name}" created successfully!', 'success')
        return redirect(url_for('firm_detail', firm_id=firm_id))
    
    return render_template('contact_form.html', firm=firm)


@app.route('/contact/<int:contact_id>/edit', methods=['GET', 'POST'])
def contact_edit(contact_id):
    """Edit existing contact"""
    contact = Contact.query.get_or_404(contact_id)
    
    if request.method == 'POST':
        contact.first_name = request.form['first_name']
        contact.last_name = request.form['last_name']
        contact.email = request.form.get('email')
        contact.phone = request.form.get('phone')
        contact.position = request.form.get('position')
        db.session.commit()
        flash(f'Contact "{contact.full_name}" updated successfully!', 'success')
        return redirect(url_for('contact_detail', contact_id=contact.id))
    
    return render_template('contact_form.html', contact=contact, firm=contact.firm)


@app.route('/project/<int:project_id>')
def project_detail(project_id):
    """Project detail page"""
    project = Project.query.get_or_404(project_id)
    notes = Note.query.filter_by(project_id=project_id).order_by(desc(Note.created_at)).all()
    return render_template('project_detail.html', project=project, notes=notes)


@app.route('/project/add/<int:firm_id>', methods=['GET', 'POST'])
def project_add(firm_id):
    """Add new project to a firm"""
    firm = Firm.query.get_or_404(firm_id)
    
    if request.method == 'POST':
        project = Project(
            name=request.form['name'],
            description=request.form.get('description'),
            status=request.form.get('status', 'Active'),
            firm_id=firm_id,
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date() if request.form.get('start_date') else None,
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d').date() if request.form.get('end_date') else None
        )
        
        # Add linked contacts
        contact_ids = request.form.getlist('contact_ids')
        for contact_id in contact_ids:
            contact = Contact.query.get(contact_id)
            if contact:
                project.contacts.append(contact)
        
        db.session.add(project)
        db.session.commit()
        flash(f'Project "{project.name}" created successfully!', 'success')
        return redirect(url_for('firm_detail', firm_id=firm_id))
    
    contacts = Contact.query.filter_by(firm_id=firm_id).all()
    return render_template('project_form.html', firm=firm, contacts=contacts)


@app.route('/project/<int:project_id>/edit', methods=['GET', 'POST'])
def project_edit(project_id):
    """Edit existing project"""
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form.get('description')
        project.status = request.form.get('status', 'Active')
        project.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date() if request.form.get('start_date') else None
        project.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date() if request.form.get('end_date') else None
        
        # Update linked contacts
        project.contacts = []
        contact_ids = request.form.getlist('contact_ids')
        for contact_id in contact_ids:
            contact = Contact.query.get(contact_id)
            if contact:
                project.contacts.append(contact)
        
        db.session.commit()
        flash(f'Project "{project.name}" updated successfully!', 'success')
        return redirect(url_for('project_detail', project_id=project.id))
    
    contacts = Contact.query.filter_by(firm_id=project.firm_id).all()
    return render_template('project_form.html', project=project, firm=project.firm, contacts=contacts)


@app.route('/note/add', methods=['POST'])
def note_add():
    """Add a note to an entity"""
    content = request.form.get('content')
    entity_type = request.form.get('entity_type')
    entity_id = request.form.get('entity_id')
    
    if not content:
        flash('Note content is required', 'error')
        return redirect(request.referrer)
    
    # Get or create a default user (in a real app, this would be the logged-in user)
    user = User.query.first()
    if not user:
        user = User(username='admin', email='admin@example.com')
        db.session.add(user)
        db.session.commit()
    
    note = Note(content=content, user_id=user.id)
    
    if entity_type == 'firm':
        note.firm_id = entity_id
    elif entity_type == 'contact':
        note.contact_id = entity_id
    elif entity_type == 'project':
        note.project_id = entity_id
    
    db.session.add(note)
    db.session.commit()
    flash('Note added successfully!', 'success')
    return redirect(request.referrer)


@app.template_filter('datetime_format')
def datetime_format(value, format='%Y-%m-%d %H:%M'):
    """Format a datetime object"""
    if value is None:
        return ''
    return value.strftime(format)


@app.template_filter('date_format')
def date_format(value, format='%Y-%m-%d'):
    """Format a date object"""
    if value is None:
        return ''
    return value.strftime(format)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

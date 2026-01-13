# Mini-CRM Development Guide

## Architecture Overview

This mini-CRM system is built with a clean architecture following Flask best practices.

### Application Structure

```
/
├── app.py              # Main Flask application with routes and views
├── models.py           # SQLAlchemy database models
├── init_db.py          # Database initialization and sample data
├── requirements.txt    # Python dependencies
├── templates/          # Jinja2 HTML templates
│   ├── base.html           # Base template with common layout
│   ├── index.html          # Homepage
│   ├── firm_*.html         # Firm-related templates
│   ├── contact_*.html      # Contact-related templates
│   └── project_*.html      # Project-related templates
├── .env.example        # Environment variables template
└── .gitignore          # Git ignore rules
```

## Database Design

### Entity Relationships

```
┌─────────────┐
│    User     │ (PVEDI Users)
│  - id       │
│  - username │
│  - email    │
└──────┬──────┘
       │
       │ creates
       ↓
   ┌───────┐
   │ Note  │
   └───┬───┘
       │ attached to
       ├──────────────────────┐
       ↓                      ↓
   ┌────────┐           ┌──────────┐
   │  Firm  │──────────→│ Contact  │
   │        │  employs  │          │
   └────┬───┘           └─────┬────┘
        │                     │
        │ has                 │ works on
        ↓                     ↓
   ┌──────────┐         ┌──────────┐
   │ Project  │←────────│ Contact  │
   │          │  many   │          │
   └──────────┘  to     └──────────┘
                 many
```

### Key Relationships
- **One-to-Many**: Firm → Contacts, Firm → Projects
- **Many-to-Many**: Project ↔ Contacts (via project_contacts table)
- **Polymorphic**: Note → Firm/Contact/Project (via nullable foreign keys)

## Features Implementation

### 1. Global Search
Location: `app.py:index()`

Searches across:
- Firm name and industry
- Contact first name, last name, and email
- Project name and description

Uses SQLAlchemy's `ilike()` for case-insensitive matching.

### 2. Recent Activity Feed
Location: `app.py:index()`

Features:
- Shows last 20 notes
- Filterable by entity type (all/firms/contacts/projects)
- Sorted by creation time (newest first)

### 3. CRUD Operations

Each entity has:
- **List view**: Overview of all items
- **Detail view**: Full information with related entities
- **Add form**: Create new item
- **Edit form**: Update existing item

### 4. Notes System

Notes can be attached to any entity:
- Timestamped with creation date
- Attributed to user (currently uses first user as default)
- Displayed on entity detail pages

## Security Considerations

### Implemented
✅ SQLAlchemy parameterized queries (prevents SQL injection)
✅ Type validation for entity IDs
✅ Error handling for date parsing
✅ Data integrity validation (contacts must belong to firm)

### For Production
⚠️ Add user authentication (Flask-Login recommended)
⚠️ Add CSRF protection (Flask-WTF)
⚠️ Use environment-based configuration
⚠️ Deploy with production WSGI server (Gunicorn + Nginx)
⚠️ Enable SSL/HTTPS
⚠️ Add rate limiting
⚠️ Implement proper session management

## Extension Ideas

### User Authentication
```python
from flask_login import LoginManager, login_required

# Add to User model
def check_password(self, password):
    return check_password_hash(self.password_hash, password)
```

### API Endpoints
```python
@app.route('/api/firms', methods=['GET'])
def api_firms():
    firms = Firm.query.all()
    return jsonify([{
        'id': f.id,
        'name': f.name,
        'industry': f.industry
    } for f in firms])
```

### Advanced Search
```python
# Add full-text search with PostgreSQL
from sqlalchemy import func

Firm.query.filter(
    func.to_tsvector('english', Firm.name).match(search_query)
).all()
```

### Export Functionality
```python
import csv
from io import StringIO

@app.route('/export/firms')
def export_firms():
    # Generate CSV of firms
    si = StringIO()
    writer = csv.writer(si)
    # ... write data
```

## Testing

### Manual Testing Checklist
- [ ] Create a new firm
- [ ] Add contacts to firm
- [ ] Create project with multiple contacts
- [ ] Add notes to all entity types
- [ ] Search for entities
- [ ] Filter activity feed
- [ ] Edit entities
- [ ] Verify relationships are maintained

### Automated Testing (Future)
```python
# tests/test_models.py
def test_firm_contacts_relationship():
    firm = Firm(name="Test Firm")
    contact = Contact(first_name="John", last_name="Doe", firm=firm)
    assert contact in firm.contacts
```

## Deployment

### Development
```bash
python app.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Example)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Performance Optimization

### Database Indexing
```python
# Add to models.py
class Firm(db.Model):
    name = db.Column(db.String(200), nullable=False, index=True)
```

### Eager Loading
```python
# Reduce N+1 queries
from sqlalchemy.orm import joinedload

firms = Firm.query.options(
    joinedload(Firm.contacts),
    joinedload(Firm.projects)
).all()
```

### Pagination
```python
@app.route('/firms')
def firms_list():
    page = request.args.get('page', 1, type=int)
    firms = Firm.query.paginate(page=page, per_page=20)
    return render_template('firms_list.html', firms=firms)
```

## Troubleshooting

### Database Issues
```bash
# Reset database
rm instance/minicrm.db
python init_db.py
```

### Import Errors
```bash
# Verify all dependencies installed
pip install -r requirements.txt --upgrade
```

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, port=5001)
```

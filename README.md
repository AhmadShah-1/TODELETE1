# Mini CRM System

A scalable mini-CRM application built with Flask and PostgreSQL (with SQLite fallback for development).

## Features

- **Core Entities**: Firms, Contacts, and Projects with full relational mapping
- **Relationship Tracking**: 
  - Contacts belong to firms
  - Projects link to firms and contacts
  - PVEDI users can associate themselves for relationship tracking
- **Timestamped Notes**: Add notes to any entity with user attribution
- **Global Search**: Search across firms, contacts, and projects
- **Activity Feed**: Filterable recent activity feed showing all notes
- **Full CRUD Operations**: Create, read, update entities through web interface

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL (optional - SQLite will be used by default)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Configure PostgreSQL:
```bash
cp .env.example .env
# Edit .env and set your DATABASE_URL
```

3. Initialize the database and add sample data:
```bash
python init_db.py
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Project Structure

```
.
├── app.py              # Main Flask application
├── models.py           # Database models (User, Firm, Contact, Project, Note)
├── init_db.py          # Database initialization and sample data
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── firm_*.html
│   ├── contact_*.html
│   └── project_*.html
└── README.md
```

## Usage

### Homepage
- **Global Search**: Use the search bar to find firms, contacts, or projects
- **Add Firm**: Click "+ Add New Firm" to create a new company
- **Activity Feed**: View recent notes with filters (All, Firms, Contacts, Projects)

### Managing Firms
- View all firms from "View All Firms" button
- Click on a firm to see details, contacts, and projects
- Add contacts and projects directly from the firm detail page
- Add notes to track interactions

### Managing Contacts
- Contacts are created within a firm
- View contact details and associated projects
- Add notes to track communications

### Managing Projects
- Projects are created within a firm
- Link multiple contacts to a project
- Track project status (Active, Completed, On Hold, Cancelled)
- Set start and end dates
- Add notes for project updates

## Database Schema

- **User**: PVEDI users (username, email)
- **Firm**: Companies (name, industry, contact info)
- **Contact**: People at firms (name, email, phone, position)
- **Project**: Work items (name, description, status, dates)
- **Note**: Timestamped notes (content, user, entity references)

## Technology Stack

- **Backend**: Flask 3.0
- **Database**: PostgreSQL / SQLite
- **ORM**: SQLAlchemy
- **Frontend**: HTML/CSS (no framework - responsive design)
🕊️ Dovepeak Projects Log (DPL)

DPL — Dovepeak Projects Log is a focused, professional Django-based project tracking system designed to help individuals or small teams manage, monitor, and complete projects without losing oversight.

It provides a structured workspace to track timelines, progress, tasks, reminders, and overall project performance.

Purpose

DPL exists to:

Prevent forgotten projects

Track deadlines and timelines

Visualize progress clearly

Centralize active and completed work

Provide a professional project workspace

It is built to be simple, clean, and business-focused.



Core Features
Authentication

Secure login-only system

Admin-managed user accounts

Session-based authentication

Protected routes



Project Management

Create, update, delete projects

Assign start date and deadline

Track status:

Not Started

In Progress

On Hold

Completed

Cancelled

Automatic overdue detection

Auto progress calculation


Task Management

Add tasks per project

Track task status:

TODO

IN_PROGRESS

DONE

Project progress auto-calculated from completed tasks

Manual fallback if no tasks exist



Reminder System

Add reminders per project

Track upcoming deadlines

Flag overdue reminders

Dashboard visibility for upcoming events


Dashboard Workspace

The main control center includes:

Total Projects

Active Projects

Completed Projects

Overdue Projects

Recent Projects

Upcoming Deadlines

Visual progress bars


Architecture

Built using:

Backend: Django

Database: SQLite (default) / PostgreSQL (production-ready)

Authentication: Django built-in auth system

Frontend: Django Templates (Bootstrap/Tailwind ready)

🗃 Data Models Overview
Project

Owner

Name

Client

Description

Start Date

Deadline

Status

Progress (auto-calculated)

Overdue detection

Created / Updated timestamps

Task

Project (FK)

Title

Description

Status

Due Date

Created / Updated timestamps

Reminder

Project (FK)

Reminder Date

Message

Sent Status

Created timestamp

d🚀 Installation
1. Clone Repository
git clone <your-repository-url>
cd dpl
2. Create Virtual Environment
python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt

If not created yet:

pip install django
4. Apply Migrations
python manage.py migrate
5. Create Superuser
python manage.py createsuperuser
6. Run Development Server
python manage.py runserver

Access:

http://127.0.0.1:8000/
🔒 Access Control

All project views require login.

Users can only see their own projects.

Admin manages users through Django admin panel.

📈 Business Logic

Project progress auto-updates when tasks change.

If progress reaches 100% → project auto-marked as COMPLETED.

If deadline passes and project not completed → flagged as overdue.

Dashboard metrics computed dynamically.

Design Philosophy

DPL follows:

Simplicity over complexity

Clarity over clutter

Flexibility without unnecessary verbosity

Production-ready structure from day one

Future Roadmap

Planned enhancements:

Email reminders

Team collaboration

File attachments

Analytics dashboard

Export reports (PDF / Excel)

REST API integration

SaaS multi-tenant support

Use Case

DPL is ideal for:

Entrepreneurs

Freelancers

Small teams

Agencies

Internal operations tracking


 Vision

Dovepeak Projects Log is designed to be the central command center for all ongoing and completed work — ensuring no project is forgotten and every deadline is respected.
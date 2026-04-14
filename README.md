# Data-Oriented-Web-Portal
This Django-based web portal centralizes hospital data visualization through interactive Power BI dashboards. It features a secure, role-based access control system to provide personalized performance indicators for healthcare professionals.

## **Project Overview**
This project was developed during a technical internship at the University Hospital Center (CHU) Hassan II in Fes. It involves the creation of a decision-support web platform designed for the visualization, management, and hierarchical exploitation of hospital data.

The main objective is to centralize performance indicators from various hospital departments through dynamic reports, while ensuring secure and filtered access based on the user's profile.

## Key Features
Data Visualization: Integration of interactive Power BI reports via iframes.

Hierarchical Access Management: Automatic report filtering based on roles (General Director, Hospital Director, Head of Department, Doctor, etc.).

Secure Authentication: Login system with session management, protection against CSRF/XSS attacks, and password hashing.

Registration System with Confirmation: Validation codes sent via email using the Brevo API (Anymail) for account activation.

Centralized Administration: Management of users, hospitals, departments, and iframes through a dedicated dashboard.

Export Functionality: Option to export reports as PDF for offline consultation.

Technologies Used
Backend
* Framework: Django (MVT Architecture)

* Language: Python

* Database: PostgreSQL

* Transactional Emails: Anymail & Brevo API

Frontend
* HTML5, CSS3, JavaScript

* Django Template Language (DTL)

Business Intelligence
* Power BI

## Installation and Setup
Clone the repository:
```bash
git clone https://github.com/your-username/portail-data-chu.git
cd portail-data-chu
```

### 1. Create a virtual environment:

```bash
python -m venv env
source env/bin/activate
```
### 2. Install dependencies:

```bash
pip install -r requirements.txt
```
### 3. Apply migrations:

```bash
python manage.py migrate
```
### 4. Run the server:

```bash
python manage.py runserver
```

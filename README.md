
# **Spam Detector**

## **Overview**  

The **Spam Detector** is an application designed to identify and report spam phone numbers efficiently. It allows users to search for phone numbers, report spam, and view spam likelihood based on user reports. The system ensures secure access with authentication and enforces a **one-report-per-user** policy to maintain integrity.  

## **Features**  

- **User Authentication** (JWT-based login/logout)  
- **Search Functionality** (by phone number or name)  
- **Spam Reporting** (Users can report a number only once)  
- **Spam Likelihood Calculation** (Based on multiple reports)    

## **Endpoints**  

### **Authentication**  
- `POST /api/login/` → Get access and refresh tokens  
- `POST /api/logout/` → Logout (invalidate tokens and logs out)  

### **Search**  
- `GET /api/search/?query=<phone_number>` → Search by phone  
- `GET /api/search/?query=<name>` → Search by name  

### **Spam Reporting**  
- `POST /api/report-spam/`  
  - **Body:** `{ "phone": "<phone_number>" }`  
  - **Response:** `{ "message": "Successfully reported spam." }`  
  - **Constraints:** A user can only report a number once.  

## **Technology Stack**  

### **Backend**  
- 🚀 [Django](https://www.djangoproject.com) – A high-level Python web framework for rapid development.  
- 🔥 [Django Rest Framework](https://www.django-rest-framework.org) – For building robust and scalable APIs.  
- 🛢️ [PostgreSQL](https://www.postgresql.org) – A powerful and reliable relational database.  
- 🔑 [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io) – Secure token-based authentication.  

# Setup
### 1. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```
```bash
### 2. Install Dependencies
pip install -r requirements.txt
```
```bash
### 3. Apply Migrations
python manage.py makemigrations
python manage.py migrate
```
```bash
### 4. Run the Server
python manage.py runserver
```

## **Database Design**  

### **1. User**  
Stores authentication details of registered users.  
- `id` (Primary Key) – Unique identifier.  
- `username` (String, Unique) – Unique username for authentication.  
- `email` (String, Unique) – Email address.  
- `password` (Hashed String) – Securely stored password.  

### **2. AllUsers**  
Contains all users (both registered and unregistered) and their associated details.  
- `id` (Primary Key) – Unique identifier.  
- `name` (String) – Name of the user.  
- `phone` (BigInteger) – Phone number.  
- `email` (EmailField, Optional) – Email address.  
- `is_registered` (Boolean) – Indicates if the user is registered in the system.  
- `spam_likelihood` (Float) – Spam risk score of the user (0.0 - 10.0).  

### **3. PersonalContacts**  
Stores the contacts saved by registered users.  
- `id` (Primary Key) – Unique identifier.  
- `owner_id` (ForeignKey → `AllUsers`) – The user who owns the contact list.  
- `contact_id` (ForeignKey → `AllUsers`) – The contact saved by the owner.  
- `created_at` (Datetime) – Timestamp when the contact was saved.  
- **Unique Constraint:** `owner_id` and `contact_id` combination must be unique (no duplicate contact pairs).  

### **4. SpamReport**  
Logs reports of spam activity.  
- `id` (Primary Key) – Unique identifier.  
- `reported_by` (ForeignKey → `AllUsers`) – The user who reported the spam.  
- `phone` (String) – The reported phone number.  
- `timestamp` (Datetime) – Timestamp of when the report was made.  
- **Spam Likelihood Update:** On saving a report, the spam likelihood of the reported phone number is updated.  

### **5. SearchIndex**  
Stores indexed data for optimized search functionality.  
- `id` (Primary Key) – Unique identifier.  
- `user` (ForeignKey → `AllUsers`) – The user whose details are indexed.  
- `name` (String, Indexed) – Full name for quick lookup.  
- `phone` (String, Indexed) – Phone number for fast search queries.  

    **Optimized for Search & Spam Detection!**

## Workflow

1. Register by entering name, phone(unique), email(optional), password.
2. Once registered successfully, login using your credentials(phone and password).
3. Logged in user can perform several actions.
    - Search by typing a name
        - The top Results are people whose names start with the search query, and then people whose names contain but don’t start with the search query.
    - Search by typing a phone number
        - If there is a registered user with that phone number, only that result is showed.
        - Otherwise, it shows all the results matching that phone number completely.(duplicate results could be seen, since it's global phone book/database)
    - Detailed Search view
        - Clicking a search result displays all the details for that person along with the spam likelihood. The person’s email is only displayed if the person is a registered user and the user who is searching is in the person’s contact list.
    - Spam reporting
        - A user can mark a number as spam so that other users can identify spammers via the global database.

## **Notes**  
- Ensure **PostgreSQL** is set up if using a custom database.  
- Update `.env` with required configurations before running.  
- Use **Postman** to test API endpoints.  

---

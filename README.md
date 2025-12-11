# Organization Management Service  
### Backend Intern Assignment – FastAPI + MongoDB (Multi-Tenant Architecture)

This project implements a **multi-tenant backend service** where each organization gets its own isolated MongoDB collection.  
A **Master Database** stores organization metadata and admin credentials.  
Dynamic collections (`org_<organization_name>`) are created for every new organization.

Technologies used: **FastAPI**, **MongoDB (Motor)**, **JWT**, **Argon2 Hashing**, **Pydantic Settings**

---

## Features

### Multi-Tenant Design
- Automatically creates a MongoDB collection for each new organization  
- Format: `org_<organization_name>`

### Master Database
Stores:
- Organization name  
- Collection reference  
- Admin reference  
- Connection details  

### Admin Authentication
- JWT-based login  
- Passwords hashed using **Argon2** (more secure than bcrypt)

###  Organization Management
- Create new organization  
- Get organization details  
- Update organization info  
- Delete organization (admin-authenticated)

---

#  Project Structure
```md
org-mgmt-service/
├─ app/
│  ├─ main.py
│  ├─ config.py
│  ├─ db.py
│  ├─ auth.py
│  ├─ schemas.py
│  ├─ routers/
│  │   ├─ orgs.py
│  │   └─ admin.py
├─ docker-compose.yml
├─ requirements.txt
├─ README.md
└─ .gitignore
```


---

#  Installation & Setup

## 1.Clone the Repository
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```
## 2.Create & Activate Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate
```
## 3.Install Dependencies
```bash
pip install -r requirements.txt
```
## If requirements file not present:
```bash
pip install fastapi uvicorn[standard] motor pydantic-settings \
passlib[argon2] argon2-cffi PyJWT python-dotenv email-validator

```

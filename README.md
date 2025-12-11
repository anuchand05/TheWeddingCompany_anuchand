# 🏢 Organization Management Service  
### Backend Intern Assignment – Multi-Tenant Architecture (FastAPI + MongoDB)

This project implements a **multi-tenant backend system** where each organization gets its own isolated MongoDB collection.  
A **Master Database** stores global metadata and admin credentials, while **JWT authentication** ensures secure tenant-level operations.

Built using **FastAPI**, **Motor**, **MongoDB**, **JWT**, and **Argon2** password hashing.

---

##  Features

###  Multi-tenant architecture  
- Each organization gets a dynamic MongoDB collection:  
  `org_<organization_name>`

###  Master Database  
Stores:
- Organization metadata  
- Collection reference  
- Admin credentials (securely hashed)  
- Connection info (if needed)

###  Admin Authentication  
- JWT-based login  
- Hashed passwords using **Argon2** (recommended modern hashing algorithm)

###  CRUD Operations for Organizations  
- Create Organization  
- Get Organization  
- Update Organization (with optional collection rename & syncing)  
- Delete Organization (admin authenticated)

All APIs are available and testable through **Swagger UI** at:

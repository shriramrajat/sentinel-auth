# SentinelAuth

SentinelAuth is a centralized identity and access control service designed to handle user authentication, permission enforcement, and secure session management across multiple applications. It abstracts security logic into a dedicated system, enabling applications to delegate trust, authorization decisions, and access validation to a single, reliable source of truth. The project is built with scalability, modularity, and real-world backend patterns in mind, reflecting how modern systems manage identity and security at scale.

## 🎯 Core Capabilities

- **User Management**: Secure user registration, profile management, and account lifecycle control
- **Authentication**: JWT-based access and refresh token system with automatic rotation
- **Authorization**: Role-based access control (RBAC) with granular permission enforcement
- **Session Management**: Multi-device support with secure refresh token handling and revocation
- **Security-First Design**: Bcrypt password hashing, token-based authentication, and no plain-text secrets

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic
- **Security**: 
  - Password Hashing: `bcrypt` via `passlib`
  - JWT Tokens: `python-jose` or `PyJWT`
- **Server**: Uvicorn
- **Architecture**: Layered (API → Service → Repository → Database)

## 🏗️ Architecture Principles

SentinelAuth follows a **strict layered architecture**:

1. **API Layer**: FastAPI routes handling HTTP requests/responses
2. **Service Layer**: Business logic for authentication, authorization, and user operations
3. **Repository Layer**: Database access and query operations
4. **Core Layer**: Security utilities, configuration, and token management

This separation ensures:
- Clear separation of concerns
- Testability and maintainability
- Scalability and modularity
- No circular dependencies

## ✅ What SentinelAuth IS

- A production-ready authentication and authorization backend
- A learning project demonstrating real-world security patterns
- A reusable identity service for multiple applications
- An implementation of industry-standard security practices

## ❌ What SentinelAuth IS NOT

- **No Frontend/UI**: This is a backend-only service (APIs accessible via Swagger UI)
- **No OAuth/Social Login**: No Google, GitHub, or third-party authentication
- **No MFA**: Multi-factor authentication is out of scope
- **No Microservices**: Single monolithic application with layered architecture
- **No NoSQL**: PostgreSQL only, no MongoDB or other databases

## 📚 Project Status

This project has Completed Version 1. All core authentication, authorization, and security features are implemented, tested, and documented.

# 🏗️ System Architecture

## Layered Design
SentinelAuth follows a strict **Layered Architecture** to ensure separation of concerns:

1.  **API Layer** (`app/api`): 
    *   **Role**: Entry point for HTTP requests.
    *   **Responsibility**: Validation (Pydantic), Auth Guards (Dependencies), Response Formatting.
    *   **Components**: `auth.py`, `users.py`, `admin.py`.

2.  **Service Layer** (`app/services`):
    *   **Role**: Business Logic.
    *   **Responsibility**: Decisions (e.g., "Is password correct?", "Rotate token").
    *   **Components**: `AuthService`, `UserService`.

3.  **Repository Layer** (`app/repositories`):
    *   **Role**: Data Access.
    *   **Responsibility**: Raw SQL/ORM operations. No business logic here.
    *   **Components**: `UserRepository`, `TokenRepository`.

4.  **Database Model** (`app/db/models`):
    *   **Role**: Schema definition.
    *   **Responsibility**: Mapping Python objects to PostgreSQL tables.

## Data Flow
Request -> API (Validate) -> Service (Decide) -> Repository (Query) -> Database
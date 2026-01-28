# 📡 API Specification (v1.0.0)

## Base URL
`http://localhost:8000/api/v1`

---

## 🔐 Authentication

### **Login**
*   **Endpoint**: `POST /auth/login`
*   **Description**: Authenticate user and receive tokens.
*   **Request Body**:
    ```json
    {
      "username": "johndoe",
      "password": "secretpassword"
    }
    ```
*   **Response (200 OK)**:
    ```json
    {
      "access_token": "eyJhbG...",
      "refresh_token": "def502...",
      "token_type": "bearer"
    }
    ```

### **Refresh Token**
*   **Endpoint**: `POST /auth/refresh`
*   **Description**: Exchange a valid refresh token for a new access/refresh pair.
*   **Request Body**:
    ```json
    {
      "refresh_token": "def502..."
    }
    ```
*   **Response (200 OK)**: *(Same as Login)*

---

## 👤 Users

### **Signup**
*   **Endpoint**: `POST /users/signup`
*   **Description**: Register a new user account.
*   **Request Body**:
    ```json
    {
      "username": "johndoe",
      "email": "john@example.com",
      "password": "secretpassword"
    }
    ```
*   **Response (201 Created)**:
    ```json
    {
      "id": "3fa85f64-...",
      "username": "johndoe",
      "email": "john@example.com",
      "is_active": true,
      "role": { "name": "user" }
    }
    ```

### **Get My Profile**
*   **Endpoint**: `GET /users/me`
*   **Headers**: `Authorization: Bearer <access_token>`
*   **Response (200 OK)**: User profile object.

### **Update My Profile**
*   **Endpoint**: `PATCH /users/me`
*   **Headers**: `Authorization: Bearer <access_token>`
*   **Request Body**: (All fields optional)
    ```json
    {
      "first_name": "Johnny",
      "email": "newemail@example.com"
    }
    ```

---

## 🛡️ Admin

### **List All Users**
*   **Endpoint**: `GET /admin/users`
*   **Headers**: `Authorization: Bearer <admin_access_token>`
*   **Query Params**: `?skip=0&limit=100`
*   **Response (200 OK)**: List of User profile objects.
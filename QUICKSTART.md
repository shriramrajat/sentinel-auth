# 🚀 Quick Start Guide - SentinelAuth

## ✅ What We've Done So Far

1. ✅ Created project structure
2. ✅ Implemented foundation files
3. ✅ Installed dependencies
4. ✅ Created `.env` file
5. ✅ Created `.gitignore`

---

## ⚠️ Current Issue

The app is trying to start but **can't connect to PostgreSQL** because:
- PostgreSQL is not installed, OR
- PostgreSQL is not running, OR
- Database `sentinelauth` doesn't exist

---

## 🔧 Next Steps - Choose Your Path

### **Option 1: Install PostgreSQL Locally (Recommended for Learning)**

#### Step 1: Install PostgreSQL
- **Windows**: Download from https://www.postgresql.org/download/windows/
- During installation, remember the password you set for `postgres` user
- Default port: `5432`

#### Step 2: Create Database
```bash
# Open PostgreSQL command line (psql)
psql -U postgres

# Create database
CREATE DATABASE sentinelauth;

# Exit
\q
```

#### Step 3: Update `.env` file
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/sentinelauth
```

#### Step 4: Run the app
```bash
uvicorn app.main:app --reload
```

---

### **Option 2: Use Docker (Fastest)**

#### Step 1: Create `docker-compose.yml` in root
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: sentinelauth
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

#### Step 2: Start PostgreSQL
```bash
docker-compose up -d
```

#### Step 3: `.env` is already configured correctly!
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sentinelauth
```

#### Step 4: Run the app
```bash
uvicorn app.main:app --reload
```

---

### **Option 3: Use SQLite (Quick Test - Not for Production)**

If you just want to test the app quickly without PostgreSQL:

#### Step 1: Update `.env`
```env
DATABASE_URL=sqlite:///./sentinelauth.db
```

#### Step 2: Install SQLite driver
```bash
pip install aiosqlite
```

#### Step 3: Run the app
```bash
uvicorn app.main:app --reload
```

**⚠️ Note**: SQLite is fine for testing, but your spec requires PostgreSQL for production.

---

## 🎯 What Happens When App Starts Successfully

You'll see:
```
🚀 Starting SentinelAuth v1.0.0
📊 Database: localhost:5432/sentinelauth
🔒 Debug Mode: True
✅ Database connection successful
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Then visit:
- **http://localhost:8000** → Root endpoint
- **http://localhost:8000/health** → Health check
- **http://localhost:8000/docs** → Swagger UI (Interactive API docs)

---

## 📝 Understanding the Error You Got

```
ValidationError: 2 validation errors for Settings
DATABASE_URL
  Field required [type=missing]
SECRET_KEY
  Field required [type=missing]
```

**This is GOOD!** 🎉

**Why?**
- Your app is using the **fail fast** principle
- It detected missing environment variables **before** starting
- This prevents serving a broken API
- Much better than crashing during a request

**What I did:**
- Created `.env` file with all required variables
- Now Pydantic will load these on startup
- App will verify DB connection before accepting requests

---

## 🔑 About the SECRET_KEY in `.env`

I generated a secure random key:
```
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

**How to generate your own:**
```python
# In Python
import secrets
print(secrets.token_hex(32))
```

**⚠️ IMPORTANT:**
- Never commit `.env` to git (already in `.gitignore`)
- Use different SECRET_KEY in production
- Keep it secret!

---

## 📦 Dependencies Installed

✅ Already installed:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `pydantic` - Data validation
- `pydantic-settings` - Settings management
- `psycopg-binary` - PostgreSQL driver
- `python-dotenv` - Load .env files

---

## 🐛 Troubleshooting

### "Database connection failed"
- Check PostgreSQL is running
- Verify credentials in `.env`
- Ensure database exists

### "Module not found"
- Make sure you're in virtual environment: `venv\Scripts\activate`
- Reinstall: `pip install -r requirements.txt` (we'll create this)

### "Port 8000 already in use"
- Kill existing process or use different port:
  ```bash
  uvicorn app.main:app --reload --port 8001
  ```

---

## ✅ Checklist

Before proceeding to build models:

- [ ] PostgreSQL installed and running
- [ ] Database `sentinelauth` created
- [ ] `.env` file configured with correct credentials
- [ ] App starts without errors
- [ ] Can access http://localhost:8000/docs
- [ ] Health check returns `{"status": "healthy"}`

---

## 🎓 What You Learned

1. **Environment Variables**: Never hardcode secrets
2. **Fail Fast**: Better to crash on startup than serve broken API
3. **Pydantic Validation**: Automatic type checking and validation
4. **Database Connection**: Verify critical resources on startup
5. **Development Setup**: Local PostgreSQL vs Docker vs SQLite

---

**Next Step**: Once PostgreSQL is running and app starts successfully, we'll build the database models! 🚀

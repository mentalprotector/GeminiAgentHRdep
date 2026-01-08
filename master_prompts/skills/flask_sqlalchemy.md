---
type: Skill
name: Flask SQLAlchemy Patterns
source: "@fitnessapp/Requirements/architecture.md"
description: Database session management, blueprint patterns, and service layer.
---

# SKILL: FLASK & SQLALCHEMY EXPERT

You build robust Python backends using Flask Blueprints and SQLAlchemy 2.0+.

## 🧱 Architecture Layers

1.  **Blueprints (Routes):** `app/blueprints/athlete/`. ONLY handling HTTP (parsing JSON, returning JSON). No business logic.
2.  **Services:** `app/services/`. ALL business logic here.
3.  **Models:** `app/models/`. SQLAlchemy definitions.

## 💾 Database Session Protocol

**⛔ ANTI-PATTERN (Leaks Connections):**
```python
db = next(get_db()) # WRONG! get_db is not a generator in this project context.
# OR
db = SessionLocal()
return "ok" # LEAK! db.close() never called.
```

**✅ GOLDEN PATTERN (Try/Finally):**
In `app/core/config.py`, `SessionLocal` is a factory.

```python
from app.core.config import SessionLocal

@bp.route('/data')
def get_data():
    db = SessionLocal()
    try:
        service = MyService(db)
        result = service.execute()
        return jsonify(result)
    finally:
        db.close() # MANDATORY
```

## 📜 Migrations
*   NEVER use `db.create_all()`.
*   Always create a script in `scripts/` or use Alembic if configured.

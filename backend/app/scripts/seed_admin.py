import os
import sys

# 1. FIX PATH REGISTRY FOR ABSOLUTE IMPORTS
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
backend_path = os.path.join(project_root, "backend")

# Ensure Python looks directly inside 'backend' so it can see 'app'
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 2. POPULATE MACHINE MEMORIES BEFORE ANY Pydantic INITIALIZATION
from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, ".env"))

# Explicitly map the lowercase variable fields to uppercase so Pydantic sees them fallback
if os.environ.get("DATABASE_URL") and not os.environ.get("database_url"):
    os.environ["database_url"] = os.environ["DATABASE_URL"]
if os.environ.get("JWT_SECRET_KEY") and not os.environ.get("jwt_secret_key"):
    os.environ["jwt_secret_key"] = os.environ["JWT_SECRET_KEY"]

# 3. STANDARD SYSTEM IMPORTS
from sqlalchemy import func, select

def main() -> None:
    # 4. LAZY LOADING (Shields Pydantic until environment variables are fully active)
    from app.core.database import SessionLocal
    from app.core.security import hash_password
    from app.models.role import UserRole
    from app.models.user import User
    from app.services import role_service

    username = os.environ.get("ADMIN_SEED_USERNAME")
    password = os.environ.get("ADMIN_SEED_PASSWORD")
    
    if not username or not password:
        sys.exit(
            "ADMIN_SEED_USERNAME and ADMIN_SEED_PASSWORD must both be set in your .env file."
        )

    email = os.environ.get("ADMIN_SEED_EMAIL") or None
    full_name = os.environ.get("ADMIN_SEED_FULL_NAME", "System Administrator")

    with SessionLocal() as db:
        role_service.ensure_core_roles_exist(db)

        existing = db.execute(
            select(User).where(func.lower(User.username) == username.lower())
        ).scalar_one_or_none()
        if existing is not None:
            print(f"User '{username}' already exists -- not creating a duplicate admin.")
            print(f"Current role: {existing.role.name}")
            return

        admin_role = role_service.get_role_by_name(db, UserRole.ADMIN)
        admin = User(
            username=username,
            email=email,
            full_name=full_name,
            password_hash=hash_password(password),
            role_id=admin_role.id,
        )
        db.add(admin)
        db.commit()
        print(f"Created initial admin '{username}'.")


if __name__ == "__main__":
    main()

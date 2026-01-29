from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.extensions import db


# -------------------------
# PASSWORD HASHING
# -------------------------
def hash_password(password: str) -> str:
    """
    Takes plain password and returns hashed password.
    """
    return generate_password_hash(password)


# -------------------------
# PASSWORD VERIFICATION
# -------------------------
def verify_password(password_hash: str, password: str) -> bool:
    """
    Verifies plain password against stored hash.
    """
    return check_password_hash(password_hash, password)


# -------------------------
# CREATE USER
# -------------------------
def create_user(username: str, password: str) -> User:
    """
    Creates a new user with hashed password.
    """
    hashed_password = hash_password(password)

    user = User(
        username=username,
        password_hash=hashed_password,
        is_verified=True   # OTP handled separately
    )

    db.session.add(user)
    db.session.commit()

    return user


# -------------------------
# AUTHENTICATE USER
# -------------------------
def authenticate_user(username: str, password: str):
    """
    Validates user credentials.
    Returns user if valid, else None.
    """
    user = User.query.filter_by(username=username).first()

    if not user:
        return None

    if not verify_password(user.password_hash, password):
        return None

    return user

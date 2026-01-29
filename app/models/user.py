from datetime import datetime
from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    password_hash = db.Column(db.String(256), nullable=False)

    is_verified = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    profile = db.relationship(
        "Profile",
        backref="user",
        uselist=False,
        cascade="all, delete"
    )

    tasks = db.relationship(
        "Task",
        backref="user",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<User {self.username}>"

from datetime import datetime
from app.extensions import db

class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    full_name = db.Column(db.String(120), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    mobile = db.Column(db.String(15), unique=True, nullable=False)

    dob = db.Column(db.Date, nullable=False)

    gender = db.Column(db.String(10), nullable=False)

    occupation = db.Column(db.String(100), nullable=False)

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Profile {self.full_name}>"

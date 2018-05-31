from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, DateTime, String, Boolean

from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    creation_date = Column(DateTime, default=datetime.now)
    modified_date = Column(DateTime, default=datetime.now)

    public_id = Column(String(50), unique=True)
    name = Column(String(50), unique=True)
    password = Column(String(80))
    admin = Column(Boolean, default=False)
    confirmed = Column(Boolean, default=False)
    active = Column(Boolean, default=False)

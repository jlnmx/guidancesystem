from app import db
from datetime import datetime
from flask_login import UserMixin


class StudentRecord(db.Model):
    __tablename__ = 'student_information'  # Correct table name

    id = db.Column(db.Integer, primary_key=True)
    lrn = db.Column(db.String(20), unique=True, nullable=False)  # Increased length
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(10))
    birthdate = db.Column(db.Date)
    mother_tongue = db.Column(db.String(50))
    religion = db.Column(db.String(50))
    barangay = db.Column(db.String(100))
    municipality_city = db.Column(db.String(100))
    father_name = db.Column(db.String(100))
    mother_name = db.Column(db.String(100))
    guardian_name = db.Column(db.String(100))
    contact_number = db.Column(db.String(15))
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    offenses = db.relationship(
        'OffenseRecord',
        backref='student',
        cascade='all, delete-orphan'  # Add cascade behavior
    )
    profile_image = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'lrn': self.lrn,
            'name': self.name,
            'grade': self.grade,
            'section': self.section,
            'sex': self.sex,
            'birthdate': self.birthdate.strftime('%Y-%m-%d') if self.birthdate else None,
            'mother_tongue': self.mother_tongue,
            'religion': self.religion,
            'barangay': self.barangay,
            'municipality_city': self.municipality_city,
            'father_name': self.father_name,
            'mother_name': self.mother_name,
            'guardian_name': self.guardian_name,
            'contact_number': self.contact_number,
            'date_time': self.date_time.strftime('%Y-%m-%d %H:%M:%S') if self.date_time else None,
            'profile_image': self.profile_image  # Include the profile image path in the dictionary
        }

class OffenseRecord(db.Model):
    __tablename__ = 'offense_record'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_information.id'), nullable=False)
    offense_type = db.Column(db.String(255), nullable=False)
    reason = db.Column(db.Text, nullable=True)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'offense_type': self.offense_type,  # <-- use the raw field name
            'reason': self.reason,
            'date_time': self.date_time.strftime('%Y-%m-%d %H:%M:%S') if self.date_time else None
        }

class User(db.Model, UserMixin):  # Move this class outside of OffenseRecord
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed passwords
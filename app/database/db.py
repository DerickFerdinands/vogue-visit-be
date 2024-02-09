# app/database/db.py
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Sequence, Boolean, Text, Date, Time
from sqlalchemy.ext.declarative import declarative_base
import bcrypt


DATABASE_URL = 'mysql+pymysql://admin:1qaz2wsx@database-1.cfsc2s82qjqy.us-east-1.rds.amazonaws.com/vogue_visit'

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(100))
    gender = Column(String(20))
    age = Column(Integer)
    email = Column(String(255), unique=True, nullable=False)
    is_salon_owner = Column(Boolean, default=False)
    hashed_password = Column(String(60), nullable=False)  # Adjust length as needed
    salon = relationship('Salon', back_populates='salon_owner')
    appointments = relationship('Appointment', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        # Hash and set the password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.hashed_password = hashed.decode('utf-8')

    def check_password(self, password):
        # Check if the provided password matches the hashed password
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"

class Salon(Base):
    __tablename__ = 'salons'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(100))
    description = Column(String(500))
    location = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'), unique=True)
    salon_owner = relationship('User', back_populates='salon')
    instagram_url = Column(String(255), unique=True)
    facebook_url = Column(String(255), unique=True)
    phone_num = Column(String(15), unique=True)
    email = Column(String(255), unique=True)
    img_1 = Column(Text)
    img_2 = Column(Text)
    img_3 = Column(Text)
    img_4 = Column(Text)
    img_5 = Column(Text)
    services = relationship('Service', back_populates='salon', cascade='all, delete-orphan')
    slots = relationship('TimeSlot', back_populates='salon', cascade='all, delete-orphan')



class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(500))
    price = Column(Integer)
    img_1 = Column(Text)
    img_2 = Column(Text)
    img_3 = Column(Text)
    img_4 = Column(Text)
    img_5 = Column(Text)
    slot_count = Column(Integer, default=1)
    salon_id = Column(Integer, ForeignKey('salons.id'))
    salon = relationship('Salon', back_populates='services')
    appointments = relationship('Appointment', back_populates='service', cascade='all, delete-orphan')


class TimeSlot(Base):
        __tablename__ = 'time_slots'
        id = Column(Integer, primary_key=True)
        salon_id = Column(Integer, ForeignKey('salons.id'))
        salon = relationship('Salon', back_populates='slots')
        date = Column(Date, nullable=False)
        start_time = Column(Time, nullable=False)
        end_time = Column(Time, nullable=False)
        is_booked = Column(Boolean, default=False)
        appointment = relationship('Appointment', back_populates='time_slot', cascade='all, delete-orphan')


class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    time_slot_id = Column(Integer, ForeignKey('time_slots.id'))
    time_slot = relationship('TimeSlot', back_populates='appointment')
    service_id = Column(Integer, ForeignKey('services.id'))
    service = relationship('Service', back_populates='appointments')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='appointments')
    payment_status = Column(Text, nullable=False, default='PENDING')
    identifier = Column(String(100), nullable=False)



# Create new tables
Base.metadata.create_all(bind=engine)

# Create Session
SessionLocal = sessionmaker( bind=engine)

def get_db():
    db = SessionLocal()
    # try:
    #     yield db
    # finally:
    #     db.close()
    return db

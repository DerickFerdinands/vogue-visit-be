# app/database/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Sequence, Boolean
from sqlalchemy.ext.declarative import declarative_base
import bcrypt


DATABASE_URL = 'mysql+pymysql://root:1234@localhost/vogue_visit'

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
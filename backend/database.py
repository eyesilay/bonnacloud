from sqlalchemy import create_engine, Column, Integer, String, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./data/bonnacloud.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RoleDB(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    allowed_folders = Column(JSON, default=[]) # Rol düzeyindeki yetkili klasörler
    
    # Rol silindiğinde veya güncellendiğinde bağlı kullanıcıları izlemek için ilişki
    users = relationship("UserDB", back_populates="role_rel")

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="müşteri") # Eski sürümlerle uyumluluk için (admin, müşteri vb.)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True) # Yeni dinamik rol bağlantısı
    company = Column(String, nullable=True)
    allowed_folders = Column(JSON, default=[]) # Bireysel özel yetki verilmek istenirse (yedek kalkan)
    is_active = Column(Boolean, default=True)
    failed_login_attempts = Column(Integer, default=0)
    lockout_until = Column(DateTime, nullable=True)

    role_rel = relationship("RoleDB", back_populates="users")
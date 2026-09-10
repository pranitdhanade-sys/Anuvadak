"""SQLAlchemy persistence: PostgreSQL in Docker, SQLite only for local tests."""
import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

load_dotenv()
_raw_url = os.getenv("DATABASE_URL", "sqlite:///./sign_language.db")
# The user-facing DATABASE_URL remains the standard PostgreSQL URL; SQLAlchemy uses psycopg v3.
DATABASE_URL = _raw_url.replace("postgresql://", "postgresql+psycopg://", 1) if _raw_url.startswith("postgresql://") else _raw_url
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
class Base(DeclarativeBase): pass
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    history: Mapped[list["TranslationHistory"]] = relationship(back_populates="user")
class TranslationHistory(Base):
    __tablename__ = "translation_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    recognized_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped[User | None] = relationship(back_populates="history")
def init_db(): Base.metadata.create_all(bind=engine)
def database_healthy() -> bool:
    try:
        with engine.connect() as connection: connection.execute(text("SELECT 1"))
        return True
    except Exception: return False
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
